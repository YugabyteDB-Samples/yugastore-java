# Testing Strategy

## Goals

1. Achieve 90%+ unit test line coverage across all in-scope microservices
2. Establish a full testing pyramid: unit → component → integration → UI → E2E/acceptance
3. Serve as a reference implementation demonstrating AI-assisted test writing
4. De-risk future technology upgrades (no toolchain upgrades are part of this work)

---

## Scope

**In scope:**
- `products-microservice`
- `cart-microservice`
- `checkout-microservice`
- `api-gateway-microservice`
- `react-ui` (Spring proxy + React frontend)

**Out of scope (deferred):**
- `eureka-server-local` — single configuration class; existing context-load test is sufficient
- `login-microservice` — WIP, not integrated into the application

---

## Testing Pyramid

Testcontainers at the component level for real DB dialect fidelity. WireMock for Feign client isolation. Playwright for E2E. No technology upgrades — tests written against the current stack.

| Layer | Scope | Tooling | Run trigger |
|---|---|---|---|
| Unit | Service, util, domain logic | JUnit 5 + Mockito | Every build |
| Component | Each microservice in isolation | `@SpringBootTest` + Testcontainers (YugabyteDB) + WireMock | Every build |
| Integration | Full deployed stack smoke tests | REST-Assured, `-P integration-tests` Maven profile | Manual / CI gate |
| UI | React component tests | Jest + `@testing-library/react` v8 | Every build |
| E2E / Acceptance | User journeys through browser | Playwright (Java), `-P e2e` Maven profile | Manual / CI gate |

---

## Structural Changes

### New Maven module
`e2e-tests/` — added to root aggregator POM, contains Playwright-based E2E and acceptance tests.

### New test resources
Each in-scope module gets `src/test/resources/application-test.yml` to configure test-scoped overrides (Testcontainers connection strings, WireMock ports, disabled Eureka registration).

### Test class naming convention

| Suffix | Type | Runs via |
|---|---|---|
| `*Test.java` | Unit | Maven Surefire (every build) |
| `*ComponentTest.java` | Component | Maven Surefire (Testcontainers starts per class) |
| `*IT.java` | Integration | Maven Failsafe (`-P integration-tests`) |
| `*E2ETest.java` | E2E / Acceptance | Maven Failsafe (`-P e2e`) |

---

## New Dependencies

| Library | Purpose | Added to |
|---|---|---|
| `org.testcontainers:yugabytedb` | Real YugabyteDB in component tests | products, cart, checkout |
| `org.springframework.cloud:spring-cloud-contract-wiremock` | Mock Feign downstream calls | api-gateway, checkout |
| `io.rest-assured:rest-assured` | HTTP assertions in integration tests | e2e-tests module |
| `org.jacoco:jacoco-maven-plugin` | Coverage measurement and enforcement | parent pom |
| `com.microsoft.playwright:playwright` | Browser-based E2E tests | e2e-tests module |
| `@testing-library/react@^8` | React 16 compatible component tests | react-ui/frontend |
| `@testing-library/jest-dom` | DOM assertion helpers for React tests | react-ui/frontend |

---

## Coverage Enforcement

JaCoCo configured at the parent POM level.

- **Threshold:** 90% line coverage minimum
- **Gate applies to:** unit + component test phases (Surefire)
- **Gate does NOT apply to:** integration, E2E layers — those test wiring, not logic
- **Excluded from measurement:** generated code, configuration classes, main application entry points, Eureka module, login-microservice

---

## Component Test Architecture

Each in-scope microservice gets its own isolated component test harness:

**YCQL services (products, checkout):**
- `@SpringBootTest(webEnvironment = RANDOM_PORT)`
- `YugabyteDBYCQLContainer` from Testcontainers
- `application-test.yml` overrides YCQL connection to container address
- WireMock stubs for any Feign clients (checkout → products, checkout → cart)

**YSQL service (cart):**
- `@SpringBootTest(webEnvironment = RANDOM_PORT)`
- `YugabyteDBYSQLContainer` from Testcontainers
- `application-test.yml` overrides Spring datasource URL to container

**Gateway (api-gateway):**
- `@SpringBootTest(webEnvironment = RANDOM_PORT)`
- No DB — WireMock stubs for all three downstream services (products, cart, checkout)
- Validates routing, request transformation, and response mapping

---

## Integration Layer

Thin smoke-test layer run against the fully deployed stack (Docker Compose or manually started services). Validates wiring and Eureka registration — not business logic (covered at component layer).

Key journeys validated:
- Product listing reachable through gateway
- Cart operations reachable through gateway
- Checkout flow reachable through gateway

---

## UI Layer (React)

`@testing-library/react` v8 installed into `react-ui/frontend` (React 16 compatible, no toolchain upgrade). Tests run via existing `npm test` script (`react-scripts test`).

Focus: product list, product card, cart view, checkout form.

---

## E2E / Acceptance Layer

Playwright (Java API) in new `e2e-tests/` Maven module. Tests run against the full local stack.

Key user journeys:
1. Browse product catalog with pagination
2. Add product to cart
3. View and modify cart
4. Complete checkout

---

## Implementation Notes

- The existing six `contextLoads()` smoke tests should be replaced (not supplemented) as each layer is built.
- The existing tests will fail in CI without live YugabyteDB + Eureka — Testcontainers and `application-test.yml` profiles fix this.
- YCQL config beans use `@Profile("local")` / `@Profile("cloud")` — the test profile must activate `local` and override the YCQL contact point to the Testcontainers host/port.
- The `POST /api/v1/shoppingCart` read pattern (cart reads are POSTs, not GETs) must be reflected in component and E2E test HTTP calls.
- Product endpoints require both `limit` and `offset` params — omitting either returns HTTP 500.
