# react-ui

Serves the React production bundle from a Spring Boot jar. Also provides a Spring MVC proxy layer that forwards browser calls to the api-gateway.

**Port:** 8080

## Spring proxy layer

`CronosProductsController` proxies all browser API calls to the api-gateway at `http://localhost:8081/api/v1/` (configurable via `cronos.yugabyte.api` in `application.yml`). The React source contains no hardcoded hostnames.

| Browser route | Proxied to |
|---|---|
| `/products` | `GET /api/v1/products` |
| `/products/category/{c}` | `GET /api/v1/products/category/{c}` |
| `/products/details` | `GET /api/v1/product/{asin}` |
| `/cart/add` | `POST /api/v1/shoppingCart/addProduct` |
| `/cart/get` | `POST /api/v1/shoppingCart` |
| `/cart/checkout` | `POST /api/v1/shoppingCart/checkout` |
| `/cart/remove` | `POST /api/v1/shoppingCart/removeProduct` |

## React source

`frontend/src/components/` — organized as `App/`, `Cart/`, `Home/`, `Main/`, `Products/`, `ShowProduct/`, `common/`.

## Build integration

`frontend-maven-plugin` downloads **Node 16.13.2** (independent of system Node) during `mvn install` and runs `npm install` + `npm run build`. The production bundle is copied into the jar's `public/` folder via `maven-antrun-plugin`.

**Hot reload:** run `npm start` from `react-ui/frontend/` under Node 16 (`nvm use 16`). `react-scripts` is pinned at 1.1.1 and fails on modern Node. The `proxy` field in `package.json` points to `:8081` for hot-reload dev mode.
