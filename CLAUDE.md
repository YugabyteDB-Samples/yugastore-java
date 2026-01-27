# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Yugastore is a microservices-based e-commerce marketplace application demonstrating distributed SQL patterns with YugabyteDB. It consists of 6 Spring Boot microservices and a React frontend, designed for multi-region and Kubernetes-native deployments.

## Architecture

### Microservices Structure
- **eureka-server-local** (port 8761): Service discovery using Netflix Eureka
- **api-gateway-microservice** (port 8081): Central gateway routing all external requests
- **products-microservice** (port 8082): Product catalog using YugabyteDB YCQL (Cassandra API)
- **cart-microservice** (port 8083): Shopping cart using YugabyteDB YSQL (PostgreSQL API)
- **checkout-microservice** (port 8086): Order processing using YugabyteDB YCQL
- **login-microservice** (port 8085): Authentication using YugabyteDB YSQL
- **react-ui** (port 8080): React frontend with Spring Boot static serving wrapper

### Database APIs
- **YCQL services** (products, checkout): Use YugabyteDB's Cassandra-compatible API via Spring Data Cassandra
- **YSQL services** (cart, login): Use YugabyteDB's PostgreSQL-compatible API via Spring Data JPA
- **Schema files**: `resources/schema.cql` (YCQL) and `resources/schema.sql` (YSQL)

### Technology Stack
- **Backend**: Java 17, Spring Boot 2.6.3, Spring Cloud 2021.0.0
- **Frontend**: React 16.2.0 with React Bootstrap and React Router
- **Database**: YugabyteDB with dual API support (YCQL + YSQL)
- **Service Discovery**: Netflix Eureka
- **Inter-service Communication**: OpenFeign declarative REST clients
- **Build**: Maven 3 with multi-module structure

## Build and Development Commands

### Building the Application
```bash
# Build all modules and Docker images
mvn -DskipTests package

# Build with tests
mvn package

# Clean build
mvn clean package
```

### Running Tests
```bash
# Run all tests
mvn test

# Run tests for specific microservice
cd products-microservice && mvn test
```

### Database Setup
```bash
# Create YCQL tables (requires YugabyteDB running)
cd resources
cqlsh -f schema.cql

# Load sample data (~6K products)
./dataload.sh

# Create YSQL tables (run in ysqlsh or psql)
# Execute schema.sql manually for PostgreSQL-compatible tables
```

### Local Development (Host-based)
Start each service in separate terminals in this order:

```bash
# 1. Service Discovery
cd eureka-server-local && mvn spring-boot:run

# 2. API Gateway
cd api-gateway-microservice && mvn spring-boot:run

# 3. Products Service
cd products-microservice && mvn spring-boot:run

# 4. Cart Service
cd cart-microservice && mvn spring-boot:run

# 5. Checkout Service
cd checkout-microservice && mvn spring-boot:run

# 6. React UI
cd react-ui && mvn spring-boot:run
```

### Docker Development
```bash
# Build images (automatically done during mvn package)
mvn -DskipTests package

# Run all services in containers
./docker-run.sh

# Stop all containers
docker stop $(docker ps -q --filter "name=yugastore")
```

### Frontend Development
```bash
# Direct React development (in react-ui/frontend/)
cd react-ui/frontend
npm install
npm start  # Runs on port 3000 with proxy to localhost:8081

# Build React for production
npm run build

# Maven-integrated React build
cd react-ui && mvn spring-boot:run
```

## Key Service URLs
- **Eureka Dashboard**: http://localhost:8761
- **Main Application**: http://localhost:8080
- **API Gateway**: http://localhost:8081
- **Individual services**: localhost:808{2,3,5,6} (products, cart, login, checkout)

## Code Structure Patterns

### Spring Boot Service Structure
Each microservice follows standard Spring Boot patterns:
- `@SpringBootApplication` main class
- `@EnableDiscoveryClient` for Eureka registration (products, checkout)
- `@EnableFeignClients` for inter-service communication (gateway, products, checkout)
- Standard Controller → Service → Repository → Entity layers

### Database Integration Patterns
- **YCQL services**: Use `@EnableCassandraRepositories` and Spring Data Cassandra
- **YSQL services**: Use `@EnableJpaRepositories` and Spring Data JPA
- Both connect to same YugabyteDB cluster with different APIs

### React Component Structure
Located in `react-ui/frontend/src/components/`:
- **App/**: Main application wrapper
- **Home/**: Homepage with featured products
- **Products/**: Product catalog and category views
- **ShowProduct/**: Individual product detail pages
- **Cart/**: Shopping cart functionality
- **Main/**: Navigation and routing
- **common/**: Shared utilities and components

### Configuration Management
- Minimal external configuration (demo-focused)
- Service-specific `application.yml` files set application names for Eureka
- Docker configuration via environment variables
- Database connections use default YugabyteDB ports (9042 for YCQL, 5433 for YSQL)

## Development Notes

### Maven Module Dependencies
- Root POM manages 7 modules with Spring Boot parent
- Docker image building integrated via exec-maven-plugin
- Frontend Maven plugin handles Node.js/npm integration for React builds
- Each microservice builds independent executable JAR

### Inter-Service Communication
- All external traffic routes through API Gateway (localhost:8081)
- Services communicate via OpenFeign clients registered through Eureka
- REST APIs follow Spring Boot conventions with `@RestController`

### Database Schema Considerations
- **cronos keyspace** (YCQL): Contains products, product_rankings, orders, product_inventory
- **PostgreSQL schema** (YSQL): Contains shopping_cart tables
- Sample data includes realistic product catalog with rankings and reviews

### Testing Strategy
- Unit tests present but minimal (reference application focus)
- Test classes named `*ApplicationTests` or `*Tests`
- Tests can be skipped with `-DskipTests` for faster builds
- No integration test suite configured

### Docker Image Naming
Images built with consistent naming: `yugastore-{service}:v0.1`
- yugastore-eureka-server:v0.1
- yugastore-apiserver:v0.1
- yugastore-products:v0.1
- yugastore-cart:v0.1
- yugastore-checkout:v0.1
- yugastore-react:v0.1

## Task Master AI Instructions
**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md
