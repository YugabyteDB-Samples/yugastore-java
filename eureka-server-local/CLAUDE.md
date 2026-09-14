# eureka-server-local

Netflix Eureka service discovery server. No business logic.

**Port:** 8761 | **Must start before all other services** — all backend services register with it on startup.

## Verification

```bash
# Confirm all four backend services registered
curl -s http://localhost:8761/eureka/apps | grep -o '<name>[A-Z-]*MICROSERVICE'
# expect: PRODUCTS-MICROSERVICE, CART-MICROSERVICE, CHECKOUT-MICROSERVICE, API-GATEWAY-MICROSERVICE
```

Dashboard: http://localhost:8761

## Entry point

`src/main/java/com/yugabyte/yugastore/eureka/YugastoreEurekaServer.java`
