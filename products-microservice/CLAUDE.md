# products-microservice

Product catalog — reads 6,276 products from YugabyteDB YCQL.

@../docs/patterns/ycql.md

**Port:** 8082

## Endpoints (internal — called by api-gateway and checkout via Feign)

| Method | Path | Description |
|---|---|---|
| GET | `/products-microservice/product/{asin}` | Single product detail |
| GET | `/products-microservice/products?limit=N&offset=N` | Paginated product list |
| GET | `/products-microservice/products/category/{category}?limit=N&offset=N` | Products by category |

Both `limit` and `offset` are required on list endpoints — omitting either returns HTTP 500.

## Key classes

| Class | Location |
|---|---|
| `ProductCatalogController` | `controller/ProductCatalogController.java` |
| `ProductServiceImpl` | `service/impl/ProductServiceImpl.java` |
| `ProductMetadataRepo` | `repo/ProductMetadataRepo.java` |
| `ProductRankingRepository` | `repo/ProductRankingRepository.java` |
| `ProductInventoryRepository` | `repo/ProductInventoryRepository.java` |
| `YugabyteYCQLConfig` | `config/YugabyteYCQLConfig.java` — YCQL session config (`@Profile("local")`) |

## Called by

- `api-gateway-microservice` (Feign client: `ProductCatalogRestClient`)
- `checkout-microservice` (Feign client: `ProductCatalogRestClient` — reads `product_inventory`)
