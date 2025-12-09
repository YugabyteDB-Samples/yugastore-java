# OpenAPI Specifications

This directory contains OpenAPI 3.0 specifications for all microservices in the Yugastore e-commerce platform.

## Service Overview

| Service | Port | Specification | Description |
|---------|------|---------------|-------------|
| API Gateway | 8081 | [api-gateway.yaml](./api-gateway.yaml) | Central entry point, routes to microservices |
| Products | 8082 | [products-microservice.yaml](./products-microservice.yaml) | Product catalog and metadata |
| Cart | 8083 | [cart-microservice.yaml](./cart-microservice.yaml) | Shopping cart operations |
| Login | 8085 | [login-microservice.yaml](./login-microservice.yaml) | User authentication |
| Checkout | 8086 | [checkout-microservice.yaml](./checkout-microservice.yaml) | Order processing |
| React UI (BFF) | 8080 | [react-ui-bff.yaml](./react-ui-bff.yaml) | Backend-for-Frontend API |

## Architecture

```
┌─────────────────┐
│   React UI      │ :8080
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  React UI BFF   │ :8080 (same service)
│  (Backend API)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   API Gateway   │ :8081
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌───────┐ ┌───────┐ ┌──────────┐
│Products│ │ Cart  │ │ Checkout │
│ :8082 │ │ :8083 │ │  :8086   │
└───────┘ └───────┘ └──────────┘
    │         │          │
    └────┬────┴──────────┘
         ▼
┌─────────────────┐
│   YugabyteDB    │
│ YCQL:9042       │
│ YSQL:5433       │
└─────────────────┘

┌─────────────────┐
│  Login Service  │ :8085 (standalone)
└─────────────────┘

┌─────────────────┐
│  Eureka Server  │ :8761 (service discovery)
└─────────────────┘
```

## Viewing the Specifications

### Swagger UI
You can use Swagger UI to view and test these specifications:

```bash
# Using Docker
docker run -p 8090:8080 -e SWAGGER_JSON=/api/api-gateway.yaml -v $(pwd):/api swaggerapi/swagger-ui

# Or visit https://editor.swagger.io and paste the YAML content
```

### Redoc
For documentation-focused viewing:

```bash
docker run -p 8090:80 -e SPEC_URL=/api/api-gateway.yaml -v $(pwd):/usr/share/nginx/html/api redocly/redoc
```

## API Endpoints Summary

### Products Microservice (`/products-microservice`)
- `GET /product/{asin}` - Get product details
- `GET /products` - List all products (paginated)
- `GET /products/category/{category}` - List products by category

### Cart Microservice (`/cart-microservice`)
- `GET /shoppingCart/addProduct` - Add product to cart
- `GET /shoppingCart/productsInCart` - Get cart contents
- `GET /shoppingCart/removeProduct` - Remove from cart
- `GET /shoppingCart/clearCart` - Clear entire cart

### Checkout Microservice (`/checkout-microservice`)
- `POST /shoppingCart/checkout` - Process checkout

### Login Microservice
- `GET /registration` - Show registration form
- `POST /registration` - Process registration
- `GET /login` - Show login form

### API Gateway (`/api/v1`)
- `GET /product/{asin}` - Get product details
- `GET /products` - List all products
- `GET /products/category/{category}` - List by category
- `POST /shoppingCart` - Get cart contents
- `POST /shoppingCart/addProduct` - Add to cart
- `POST /shoppingCart/removeProduct` - Remove from cart
- `POST /shoppingCart/checkout` - Process checkout

### React UI BFF
- `GET /api/hello` - Health check
- `GET /products` - Homepage products
- `GET /products/category/{category}` - Category products
- `GET /products/details` - Product details
- `POST /cart/add` - Add to cart
- `POST /cart/get` - Get cart
- `POST /cart/remove` - Remove from cart
- `POST /cart/checkout` - Checkout

## Validation

Validate the OpenAPI specifications using:

```bash
# Using npm
npx @apidevtools/swagger-cli validate api-gateway.yaml

# Using Docker
docker run --rm -v $(pwd):/spec openapitools/openapi-generator-cli validate -i /spec/api-gateway.yaml
```
