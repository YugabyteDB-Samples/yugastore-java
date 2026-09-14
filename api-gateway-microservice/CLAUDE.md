# api-gateway-microservice

Single external entry point. The React UI calls only this service. Delegates all requests to backend services via Feign + Eureka discovery. No direct database access.

@../docs/patterns/spring-cloud.md

**Port:** 8081

## Public API routes

| Method | Path | Delegates to |
|---|---|---|
| GET | `/api/v1/product/{asin}` | products-microservice |
| GET | `/api/v1/products?limit=N&offset=N` | products-microservice |
| GET | `/api/v1/products/category/{category}?limit=N&offset=N` | products-microservice |
| POST | `/api/v1/shoppingCart` | cart-microservice (list cart) |
| POST | `/api/v1/shoppingCart/addProduct?asin=X` | cart-microservice |
| POST | `/api/v1/shoppingCart/removeProduct?asin=X` | cart-microservice |
| POST | `/api/v1/shoppingCart/checkout` | checkout-microservice |

## Feign clients

| Client | Targets |
|---|---|
| `ProductCatalogRestClient` | `products-microservice` |
| `ShoppingCartRestClient` | `cart-microservice` |
| `CheckoutRestClient` | `checkout-microservice` |

Feign clients live in `rest/clients/`. Each is a `@FeignClient`-annotated interface whose method signatures match the internal endpoint paths of the target service.

## Key classes

| Class | Location |
|---|---|
| `ProductCatalogController` | `controller/ProductCatalogController.java` |
| `ShoppingCartController` | `controller/ShoppingCartController.java` |
| `SecurityConfiguration` | `config/SecurityConfiguration.java` — CSRF/auth disabled for local dev |
