Start all services locally and open Chrome to the website.

Follow the instructions in `.claude/agents/run-local.md` to:

1. **Start Docker infrastructure** (PostgreSQL, Eureka)
2. **Start Python microservices** in background:
   - products-service (port 8082)
   - cart-service (port 8083)
   - checkout-service (port 8084)
   - login-service (port 8085)
   - api-gateway (port 8081)
3. **Start Next.js frontend** on port **1123**
4. **Open Chrome** to http://localhost:1123

Run services in background where possible to avoid blocking. Report the status of each service as it starts.
