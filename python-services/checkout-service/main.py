import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import py_eureka_client.eureka_client as eureka_client
import os
from .database import create_db_and_tables
from .routers import checkout

# Configuration
EUREKA_SERVER = os.getenv("EUREKA_URI", "http://localhost:8761/eureka")
APP_NAME = "checkout-microservice"
INSTANCE_PORT = int(os.getenv("PORT", 8084)) # Using 8084 to avoid conflict if needed, though original was 8086

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=APP_NAME,
        instance_port=INSTANCE_PORT
    )
    create_db_and_tables()
    yield
    # Shutdown
    await eureka_client.stop_async()

app = FastAPI(lifespan=lifespan, title="Checkout Microservice")

app.include_router(checkout.router)

@app.get("/health")
def health_check():
    return {"status": "UP"}

if __name__ == "__main__":
    uvicorn.run("checkout-service.main:app", host="0.0.0.0", port=INSTANCE_PORT, reload=True)
