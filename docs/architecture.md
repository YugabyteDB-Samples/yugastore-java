# Architecture

## Service map

| Service | Port | Datastore | Role |
|---|---|---|---|
| react-ui | 8080 | — | Serves React bundle; proxies browser calls to api-gateway |
| api-gateway-microservice | 8081 | — | Single external entry point; routes to backend services via Feign |
| products-microservice | 8082 | YCQL | Product catalog (6,276 products) |
| cart-microservice | 8083 | YSQL | Shopping cart |
| login-microservice | 8085 | YSQL | Auth — WIP, optional |
| checkout-microservice | 8086 | YCQL | Checkout + inventory management |
| eureka-server-local | 8761 | — | Service discovery (Netflix Eureka) |
| YugabyteDB admin UI | 15433 | — | DB admin panel |

## Call graph

```
Browser
  └─► react-ui:8080  (Spring MVC proxy)
        └─► api-gateway:8081  (Feign via Eureka)
              ├─► products-microservice:8082
              ├─► cart-microservice:8083
              └─► checkout-microservice:8086
                    ├─► cart-microservice:8083     (reads cart)
                    └─► products-microservice:8082  (checks inventory)
```

## Startup order

1. Start YugabyteDB Docker container
2. `eureka-server-local` — wait until `http://localhost:8761` responds
3. `products-microservice`, `cart-microservice`, `checkout-microservice`, `api-gateway-microservice` in parallel
4. Wait ~60 seconds for Eureka registrations to settle
5. `react-ui`

`login-microservice` is optional and not needed for the store to function.

## Build

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@17   # adjust if your JDK 17 lives elsewhere
JAVA_HOME=$JAVA_HOME ./mvnw -DskipTests -Dexec.skip=true install
```

`-Dexec.skip=true` skips the per-module `docker build` steps. `install` (not `package`) puts the parent POM in the local Maven repo so modules resolve it when run standalone.

## Inter-service communication

All backend services register with Eureka on startup. The api-gateway and checkout-microservice use Spring Cloud OpenFeign to call other services by Eureka app name — no hardcoded hosts. `EUREKA_URI` env var overrides the default `http://localhost:8761/eureka`.

## Full runbook

See [docs/RUNNING_LOCALLY.md](RUNNING_LOCALLY.md) for the complete procedure: DB setup, schema creation, data loading, service startup, verification, and troubleshooting.
