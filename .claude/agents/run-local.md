# Run Local Agent

Start all Python microservices and the Next.js frontend locally for development.

## Instructions

### 1. Prerequisites Check

Verify required tools are installed:
```bash
python3 --version
node --version
npm --version
```

### 2. Start Infrastructure (Docker)

Start PostgreSQL and Eureka server using Docker:
```bash
cd python-services
docker-compose up -d postgres eureka-server
```

Wait for services to be healthy before proceeding.

### 3. Start Python Microservices

Start each Python service in the background. Each service runs on its designated port:

| Service | Port | Directory |
|---------|------|-----------|
| products-service | 8082 | python-services/products-service |
| cart-service | 8083 | python-services/cart-service |
| checkout-service | 8084 | python-services/checkout-service |
| login-service | 8085 | python-services/login-service |
| api-gateway | 8081 | python-services/api-gateway |

For each service:
```bash
cd python-services/<service-name>
pip install -r requirements.txt  # if needed
python -m uvicorn main:app --host 0.0.0.0 --port <PORT> &
```

Environment variables needed:
- `DATABASE_URL=postgresql://postgres:password@localhost:5432/bookstore`
- `EUREKA_URI=http://localhost:8761/eureka`

### 4. Start Next.js Frontend

Start the frontend on port 1123:
```bash
cd nextjs-frontend
npm install  # if needed
npm run dev -- -p 1123
```

### 5. Open Browser

After all services are running, open Chrome to the frontend:
```bash
# macOS
open -a "Google Chrome" http://localhost:1123

# Linux
google-chrome http://localhost:1123 || xdg-open http://localhost:1123

# Windows
start chrome http://localhost:1123
```

### 6. Health Checks

Verify services are running:
- Frontend: http://localhost:1123
- API Gateway: http://localhost:8081/health
- Products: http://localhost:8082/health
- Cart: http://localhost:8083/health
- Checkout: http://localhost:8084/health
- Login: http://localhost:8085/health
- Eureka: http://localhost:8761

## Cleanup

To stop all services:
```bash
# Kill Python services
pkill -f "uvicorn"

# Stop Docker services
cd python-services && docker-compose down

# Kill Next.js
pkill -f "next dev"
```

## Troubleshooting

- If a port is already in use, kill the process: `lsof -ti:<PORT> | xargs kill -9`
- If database connection fails, ensure PostgreSQL is running and healthy
- If Eureka registration fails, services will still work but won't be discoverable
