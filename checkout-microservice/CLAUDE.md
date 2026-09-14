# checkout-microservice

Orchestrates checkout: reads the cart, checks inventory, decrements stock, creates an order record.

@../docs/patterns/ycql.md

**Port:** 8086

## Endpoint

| Method | Path | Description |
|---|---|---|
| POST | `/checkout-microservice/shoppingCart/checkout` | Execute checkout for current user |

## Checkout flow

1. Retrieve cart contents via `ShoppingCartRestClient` (Feign → cart-microservice)
2. For each item: read `product_inventory.quantity` via `ProductInventoryRepository`
3. If insufficient stock: throw `NotEnoughProductsInStockException` → HTTP 400
4. Decrement inventory and write an `orders` record to YCQL keyspace `cronos`

## Key classes

| Class | Location |
|---|---|
| `CheckoutController` | `controller/CheckoutController.java` |
| `CheckoutServiceImpl` | `service/CheckoutServiceImpl.java` |
| `ShoppingCartRestClient` | `rest/clients/ShoppingCartRestClient.java` — Feign → cart-microservice |
| `ProductCatalogRestClient` | `rest/clients/ProductCatalogRestClient.java` — Feign → products-microservice |
| `ProductInventoryRepository` | `repositories/ProductInventoryRepository.java` |
| `NotEnoughProductsInStockException` | `exception/NotEnoughProductsInStockException.java` |
| `YugabyteLocalConfig` | `config/YugabyteLocalConfig.java` — YCQL session (`@Profile("local")`) |

## Called by

- `api-gateway-microservice` (Feign client: `CheckoutRestClient`)
