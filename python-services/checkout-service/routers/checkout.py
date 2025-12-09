import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
import uuid
import os
from typing import Dict, Any
from ..database import get_session
from ..models import Order, ProductInventory
from pydantic import BaseModel

router = APIRouter(prefix="/checkout-microservice", tags=["checkout"])

# External Service URLs (resolved via Eureka or env vars)
# In a real eureka setup, we'd lookup by name. For simplicity/direct connection:
PRODUCTS_SERVICE_URL = os.getenv("PRODUCTS_SERVICE_URL", "http://products-microservice:8082/products-microservice")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-microservice:8083/cart-microservice")

class CheckoutStatus(BaseModel):
    orderNumber: str
    status: str
    orderDetails: str

@router.post("/shoppingCart/checkout", response_model=CheckoutStatus)
async def checkout(
    userid: str = "u1001", # Default as per original code
    session: Session = Depends(get_session)
):
    try:
        # 1. Get Cart Items
        async with httpx.AsyncClient() as client:
            cart_resp = await client.get(f"{CART_SERVICE_URL}/shoppingCart/productsInCart", params={"userid": userid})
            if cart_resp.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch cart")
            products_in_cart: Dict[str, int] = cart_resp.json()

        if not products_in_cart:
            return CheckoutStatus(orderNumber="", status="FAILURE", orderDetails="Cart is empty")

        order_details_str = "Customer bought these Items: "
        total_price = 0.0

        # Start Transaction (Implicit in Session)
        # 2. Check and Update Inventory
        for asin, quantity in products_in_cart.items():
            # Get Product Metadata (Price, Title)
            async with httpx.AsyncClient() as client:
                prod_resp = await client.get(f"{PRODUCTS_SERVICE_URL}/product/{asin}")
                if prod_resp.status_code != 200:
                    raise HTTPException(status_code=404, detail=f"Product {asin} not found")
                product_data = prod_resp.json()
            
            # Lock row for update (if supported) or just get
            inventory = session.get(ProductInventory, asin)
            if not inventory:
                # Should probably create if missing, or error? Java code defaulted to null/error
                raise HTTPException(status_code=404, detail=f"Inventory for {asin} not found")
            
            if inventory.quantity < quantity:
                return CheckoutStatus(
                    orderNumber="", 
                    status="FAILURE", 
                    orderDetails=f"Product is Out of Stock: {product_data.get('title')}"
                )
            
            # Deduct inventory
            inventory.quantity -= quantity
            session.add(inventory)
            
            # Accumulate details
            price = product_data.get('price', 0.0) or 0.0
            title = product_data.get('title', 'Unknown')
            total_price += price * quantity
            order_details_str += f" Product: {title}, Quantity: {quantity};"

        order_details_str += f" Order Total is : {total_price}"

        # 3. Create Order
        order_id = str(uuid.uuid4())
        new_order = Order(
            order_id=order_id,
            user_id=1, # Hardcoded as per original
            order_details=order_details_str,
            order_time=str(datetime.now()),
            order_total=total_price
        )
        session.add(new_order)
        
        session.commit()

        # 4. Clear Cart
        async with httpx.AsyncClient() as client:
            await client.get(f"{CART_SERVICE_URL}/shoppingCart/clearCart", params={"userid": userid})

        return CheckoutStatus(
            orderNumber=order_id,
            status="SUCCESS",
            orderDetails=order_details_str
        )

    except Exception as e:
        session.rollback()
        print(f"Checkout error: {e}")
        return CheckoutStatus(orderNumber="", status="FAILURE", orderDetails=f"Error: {str(e)}")
