# cart-microservice

Shopping cart — reads and writes the `shopping_cart` table in YugabyteDB YSQL.

@../docs/patterns/ysql.md

**Port:** 8083

## Endpoints (internal — called by api-gateway and checkout via Feign)

All endpoints are **POST**, including reads.

| Method | Path | Description |
|---|---|---|
| POST | `/cart-microservice/shoppingCart/addProduct?asin=X` | Add item to cart |
| POST | `/cart-microservice/shoppingCart/productsInCart` | List cart contents |
| POST | `/cart-microservice/shoppingCart/removeProduct?asin=X` | Remove item |
| POST | `/cart-microservice/shoppingCart/clearCart` | Empty cart |

## Key classes

| Class | Location |
|---|---|
| `ShoppingCartController` | `controller/ShoppingCartController.java` |
| `ShoppingCartImpl` | `service/ShoppingCartImpl.java` |
| `ShoppingCartRepository` | `repositories/ShoppingCartRepository.java` |
| `ShoppingCart` | `domain/ShoppingCart.java` — JPA entity |
| `ShoppingCartKey` | `domain/ShoppingCartKey.java` — composite PK (`user_id`, `asin`) |

## Called by

- `api-gateway-microservice` (Feign client: `ShoppingCartRestClient`)
- `checkout-microservice` (Feign client: `ShoppingCartRestClient` — reads cart at checkout)
