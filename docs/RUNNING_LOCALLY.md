# Running Yugastore locally

Verified working procedure for bringing up the whole stack (YugabyteDB + 5 Spring Boot
services + React UI) on a developer laptop. Written for agents and developers who need a
known-good path rather than the general instructions in the root [README](../README.md).

The root README assumes `mvn`, JDK 17, and a native YugabyteDB install are already present.
This doc covers the case where they are not, and records the gotchas that cost time.

- **Reference platform:** macOS (Apple Silicon, arm64), Docker Desktop available.
- **End result:** the store at <http://localhost:8080>, serving ~6,276 real products.

---

## Prerequisites

| Need | Why | If missing |
| --- | --- | --- |
| **JDK 17** | Root [pom.xml](../pom.xml) sets `maven.compiler.source/target` to 17. JDK 14 or 11 will not compile it. | `brew install openjdk@17`. Do **not** rely on the active `java` — pass `JAVA_HOME` explicitly (see below). |
| **Maven** | Build tool. | Not needed — use the bundled `./mvnw` wrapper. |
| **Docker** | Runs YugabyteDB. | Required for this procedure. |
| **Python 3** | [resources/parse_metadata_json.py](../resources/parse_metadata_json.py) turns `products.json` into loader CSVs. | `brew install python3`. Any Python 3.x works. |

Pin the JDK for every Maven and `java` command in this doc:

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17   # adjust if your JDK 17 lives elsewhere
export JAVA=$JAVA_HOME/bin/java
```

Run everything below from the repository root unless stated otherwise.

---

## Step 1: Start YugabyteDB

There is no need to install YugabyteDB natively. One container provides both APIs the app
needs — YCQL on `9042` (products, checkout) and YSQL on `5433` (cart).

```bash
docker run -d --name yugastore-db \
  -p 7000:7000 -p 9000:9000 -p 15433:15433 -p 5433:5433 -p 9042:9042 \
  yugabytedb/yugabyte:2.20.7.0-b58 \
  bin/yugabyted start --daemon=false --background=false
```

Startup takes roughly 60–90 seconds. Wait for it before continuing:

```bash
docker logs yugastore-db 2>&1 | grep -q 'YugabyteDB Started' && echo ready
```

The admin UI is at <http://localhost:15433>.

> **Gotcha — `ycqlsh` needs an explicit host.** Inside the container, YCQL binds to the
> container hostname, not `127.0.0.1`. Bare `bin/ycqlsh` fails with
> `Connection refused`; always pass `$(hostname)`. `ysqlsh` needs `-h $(hostname)` for the
> same reason.

> **On subsequent sessions** the container already exists. Use `docker start yugastore-db`
> instead of `docker run` — the data persists, so Steps 2 and 3 do not need repeating.

## Step 2: Create the schemas

```bash
docker cp resources/schema.cql yugastore-db:/tmp/schema.cql
docker cp resources/schema.sql yugastore-db:/tmp/schema.sql

# YCQL: keyspace `cronos` — products, product_rankings, product_inventory, orders
docker exec yugastore-db bash -lc 'bin/ycqlsh $(hostname) -f /tmp/schema.cql'

# YSQL: the shopping_cart table
docker exec yugastore-db bash -lc \
  'bin/ysqlsh -h $(hostname) -p 5433 -U yugabyte -d postgres -f /tmp/schema.sql'
```

Verify: `docker exec yugastore-db bash -lc 'bin/ycqlsh $(hostname) -e "DESCRIBE TABLES;"'`
should list four tables under `Keyspace cronos`.

Note that [cart-microservice](../cart-microservice/src/main/resources/application.yml) connects
as user `postgres`, while the commands above use `yugabyte`. Both are superuser roles under
YugabyteDB's default trust auth, so this works either way.

## Step 3: Load the sample data

```bash
cd resources
python3 parse_metadata_json.py products.json    # writes three CSVs, ~30s
./cassandra-loader -f cronos_products.csv -host localhost \
  -schema "cronos.products(asin, title, description, price, imUrl, also_bought, also_viewed, bought_together, buy_after_viewing, brand, categories,num_reviews,num_stars,avg_stars)" \
  -maxInsertErrors 10000 -maxErrors 10000 -charsPerColumn 256000
./cassandra-loader -f cronos_product_rankings.csv -host localhost \
  -schema "cronos.product_rankings(asin, category, sales_rank, title, price, imurl, num_reviews, num_stars, avg_stars)" \
  -maxInsertErrors 10000 -maxErrors 10000 -charsPerColumn 256000
./cassandra-loader -f cronos_product_inventory.csv -host localhost \
  -schema "cronos.product_inventory(asin, quantity)"
cd ..
```

This is exactly what [resources/dataload.sh](../resources/dataload.sh) runs; the steps are
spelled out here so a partial failure is easier to diagnose. Expect
**6,276 products / 6,022 rankings / 6,276 inventory rows** inserted.

`cassandra-loader` is a self-extracting JAR and runs fine under any modern JDK.

> **Gotcha — expected stack traces.** The products load prints
> `SetParser.parseIt` exceptions for rows whose `categories` set is malformed in the source
> data. These are per-field warnings, not failures. Trust the summary line
> (`number of lines processed: 6276 (6276 inserted)`), not the absence of traces.

> **Clean up afterward.** The load leaves untracked files in the working tree: `*.csv` in
> `resources/`, and one or two `jffi*.dylib` files in whichever directory you ran from.
> ```bash
> rm -f resources/*.csv* jffi*.dylib
> ```

## Step 4: Build

```bash
JAVA_HOME=$JAVA_HOME ./mvnw -DskipTests -Dexec.skip=true install
```

Takes about three minutes. Two flags matter:

- `-Dexec.skip=true` skips the `exec-maven-plugin` executions that shell out to
  `docker build` for each service's image. You do not need images to run on the host, and
  skipping saves several minutes.
- `install` (rather than `package`) puts the parent POM in your local repository, so each
  module resolves it when run on its own.

The `react-ui` module downloads its **own Node 16.13.2** via `frontend-maven-plugin` and
builds the production bundle into the jar. Your system Node is not used and does not
need to match.

## Step 5: Start the services

Eureka must be up first — the others register with it on startup.

```bash
LOGS=/tmp/yugastore-logs && mkdir -p $LOGS

$JAVA -jar eureka-server-local/target/eureka-server-local-0.0.1-SNAPSHOT.jar > $LOGS/eureka.log 2>&1 &
# wait for Eureka before continuing
until curl -sf http://localhost:8761/ >/dev/null; do sleep 3; done

$JAVA -jar products-microservice/target/products-microservice-0.0.1-SNAPSHOT.jar   > $LOGS/products.log 2>&1 &
$JAVA -jar cart-microservice/target/cart-microservice-0.0.1-SNAPSHOT.jar           > $LOGS/cart.log     2>&1 &
$JAVA -jar checkout-microservice/target/checkout-microservice-0.0.1-SNAPSHOT.jar   > $LOGS/checkout.log 2>&1 &
$JAVA -jar api-gateway-microservice/target/api-gateway-microservice-0.0.1-SNAPSHOT.jar > $LOGS/gateway.log 2>&1 &
sleep 60
$JAVA -jar react-ui/target/react-ui-0.0.1-SNAPSHOT.jar > $LOGS/react-ui.log 2>&1 &
```

`login-microservice` is a work in progress and is not needed for the store to function.

Running the jars directly is simpler than `mvn spring-boot:run` per service (the README's
approach) because it needs no extra Maven processes; either works.

---

## Verifying it works

Check that all four services registered:

```bash
curl -s http://localhost:8761/eureka/apps | grep -o '<name>[A-Z-]*MICROSERVICE'
```

Expect `PRODUCTS-MICROSERVICE`, `CART-MICROSERVICE`, `CHECKOUT-MICROSERVICE`,
`API-GATEWAY-MICROSERVICE`. Send no `Accept: application/json` header — the JSON
representation nests names differently and the `grep` above will not match it. The
dashboard at <http://localhost:8761> shows the same thing in a table.

Then exercise the two database paths end to end:

```bash
# YCQL read path, through the UI's proxy
curl -s 'http://localhost:8080/products?limit=2&offset=0'
curl -s 'http://localhost:8080/products/category/Books?limit=2&offset=0'

# YSQL write path: add to cart (POST), then confirm the row landed
curl -s -X POST 'http://localhost:8081/api/v1/shoppingCart/addProduct?asin=1049830512'
docker exec yugastore-db bash -lc \
  'bin/ysqlsh -h $(hostname) -p 5433 -U yugabyte -d postgres -c "SELECT * FROM shopping_cart;"'
```

Both product calls should return JSON arrays; the cart call returns `{"1049830512":1}` and
leaves one row in `shopping_cart`. Delete the test row when done:

```bash
docker exec yugastore-db bash -lc \
  "bin/ysqlsh -h \$(hostname) -p 5433 -U yugabyte -d postgres -c \"DELETE FROM shopping_cart WHERE user_id = 'u1001';\""
```

Finally, open <http://localhost:8080>.

---

## Service map

| Service | Port | Datastore |
| --- | --- | --- |
| React UI (Spring Boot serving the built bundle) | [8080](http://localhost:8080) | — |
| API gateway — the only service the UI talks to | 8081 | — |
| Products | 8082 | YCQL |
| Cart | 8083 | YSQL |
| Checkout + inventory | 8086 | YCQL |
| Login (work in progress, optional) | 8085 | YSQL |
| Eureka discovery | [8761](http://localhost:8761) | — |
| YugabyteDB admin UI | [15433](http://localhost:15433) | — |

The UI's own Spring controller proxies the browser's relative `/products...` calls to the
gateway, per `cronos.yugabyte.api` in
[react-ui/src/main/resources/application.yml](../react-ui/src/main/resources/application.yml).
The React source therefore contains no hostnames.

---

## Troubleshooting

**`HTTP 500` with `Optional int parameter 'limit'/'offset' ... cannot be translated into a
null value`** — not a bug. `/products` and `/products/category/{c}` require **both** `limit`
and `offset` as query params. Always send `?limit=N&offset=0`.

**`HTTP 405 Method Not Allowed` on a cart endpoint** — the gateway's cart and checkout
endpoints are **POST**, including the ones that only read
(`POST /api/v1/shoppingCart` lists the cart). Only the product endpoints are GET.

**`HTTP 404` or `500` on `http://localhost:8081/`, `:8082/`, `:8086/`** — expected. These
services define no root mapping. Test a real endpoint instead.

**A category page returns `[]`** — the category name probably does not exist. Real values
include `Books`, `Beauty`, `Music`, `Movies & TV`, `Toys & Games`,
`Cell Phones & Accessories`. Some are stored HTML-escaped in the source data
(`Home&amp;Kitchen`, `Sports&amp;Outdoors`) — a pre-existing quirk of the sample dataset,
not of the load procedure. List them with:

```bash
docker exec yugastore-db bash -lc \
  'bin/ycqlsh $(hostname) -e "SELECT category FROM cronos.product_rankings LIMIT 300;"'
```

**Build fails on a `switch` expression, `record`, or similar** — a pre-17 JDK is in use.
Confirm with `$JAVA_HOME/bin/java -version`; the active `java` on `PATH` is irrelevant as
long as `JAVA_HOME` is passed to `./mvnw`.

**A service exits immediately** — check its log in `$LOGS`. The usual cause is a port
already in use or YugabyteDB not being up yet.

---

## Frontend hot reload

The procedure above serves the **production bundle** from the `react-ui` jar, so UI edits
require a rebuild. `npm start` in `react-ui/frontend` would give hot reload and proxies to
`:8081` via the `proxy` field in its `package.json` — but `react-scripts` is pinned at
**1.1.1**, which fails on modern Node. If you need hot reload, run it under Node 16
(`nvm use 16`), ideally the same version the Maven build pins.

## Shutting down

```bash
pkill -f 'yugastore|microservice|eureka-server-local|react-ui'   # or kill the recorded PIDs
docker stop yugastore-db
```

The container retains its data. Next session: `docker start yugastore-db`, then Step 5 —
Steps 2 and 3 are one-time.
