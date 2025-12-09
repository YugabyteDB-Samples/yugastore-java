from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, col
from datetime import datetime
from typing import Dict, List, Optional
from ..database import get_session
from ..models import ShoppingCart

router = APIRouter(prefix="/cart-microservice", tags=["cart"])

def get_cart_key(user_id: str, asin: str) -> str:
    return f"{user_id}-{asin}"

@router.get("/shoppingCart/addProduct")
def add_product_to_cart(
    userid: str = Query(..., alias="userid"),
    asin: str = Query(..., alias="asin"),
    session: Session = Depends(get_session)
):
    cart_key = get_cart_key(userid, asin)
    cart_item = session.get(ShoppingCart, cart_key)
    
    if cart_item:
        cart_item.quantity += 1
        session.add(cart_item)
    else:
        cart_item = ShoppingCart(
            cart_key=cart_key,
            user_id=userid,
            asin=asin,
            quantity=1,
            time_added=str(datetime.now())
        )
        session.add(cart_item)
    
    session.commit()
    return "Added to Cart"

@router.get("/shoppingCart/productsInCart")
def get_products_in_cart(
    userid: str = Query(..., alias="userid"),
    session: Session = Depends(get_session)
) -> Dict[str, int]:
    statement = select(ShoppingCart).where(ShoppingCart.user_id == userid)
    cart_items = session.exec(statement).all()
    
    result = {}
    for item in cart_items:
        result[item.asin] = item.quantity
    
    return result

@router.get("/shoppingCart/removeProduct")
def remove_product_from_cart(
    userid: str = Query(..., alias="userid"),
    asin: str = Query(..., alias="asin"),
    session: Session = Depends(get_session)
):
    cart_key = get_cart_key(userid, asin)
    cart_item = session.get(ShoppingCart, cart_key)
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            session.add(cart_item)
            session.commit()
        else:
            session.delete(cart_item)
            session.commit()
            
    return "Removing from Cart"

@router.get("/shoppingCart/clearCart")
def clear_cart(
    userid: str = Query(..., alias="userid"),
    session: Session = Depends(get_session)
):
    # This is slightly less efficient in logic than the raw SQL delete but works with ORM
    statement = select(ShoppingCart).where(ShoppingCart.user_id == userid)
    cart_items = session.exec(statement).all()
    
    for item in cart_items:
        session.delete(item)
    
    session.commit()
    return "Clearing Cart, Checkout successful"
