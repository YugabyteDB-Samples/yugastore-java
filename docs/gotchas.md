# Cross-cutting gotchas

**ycqlsh/ysqlsh need an explicit host inside the container** — YCQL and YSQL both bind to the container hostname, not `127.0.0.1`. Always use `$(hostname)`:

```bash
docker exec yugastore-db bash -lc 'bin/ycqlsh $(hostname) -e "YOUR CQL"'
docker exec yugastore-db bash -lc 'bin/ysqlsh -h $(hostname) -p 5433 -U yugabyte -d postgres -c "YOUR SQL"'
```

**Cart endpoints are POST — including reads** — `POST /api/v1/shoppingCart` lists the cart contents. Only the product catalog endpoints are GET.

**Product endpoints require both `limit` and `offset`** — omitting either returns HTTP 500. Always send `?limit=N&offset=0`.

**Startup timing** — services take ~60 seconds after launch to register with Eureka and become healthy. `react-ui` must start last, after the backend services are registered.

**Yugabyte Java Driver, not DataStax** — `products-microservice` and `checkout-microservice` use `com.yugabyte:java-driver-core:4.6.0-yb-10`, which is explicitly added while the OSS DataStax driver is excluded from `spring-boot-starter-data-cassandra`. Do not add DataStax driver dependencies to those modules.

**Spring profile `local` vs `cloud`** — YCQL config beans are annotated `@Profile("local")` or `@Profile("cloud")`. The default active profile is `local`; no extra env var is needed for local dev.
