from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from ..database import get_session
from ..models import ProductMetadata, ProductRanking

router = APIRouter(prefix="/products-microservice", tags=["products"])

@router.get("/product/{asin}", response_model=ProductMetadata)
def get_product_details(asin: str, session: Session = Depends(get_session)):
    product = session.get(ProductMetadata, asin)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/products", response_model=List[ProductMetadata])
def get_products(
    limit: int = Query(10, ge=1), 
    offset: int = Query(0, ge=0), 
    session: Session = Depends(get_session)
):
    statement = select(ProductMetadata).offset(offset).limit(limit)
    products = session.exec(statement).all()
    return products

@router.get("/products/category/{category}", response_model=List[ProductRanking])
def get_products_by_category(
    category: str, 
    limit: int = Query(10, ge=1), 
    offset: int = Query(0, ge=0), 
    session: Session = Depends(get_session)
):
    statement = select(ProductRanking).where(ProductRanking.category == category).offset(offset).limit(limit)
    rankings = session.exec(statement).all()
    return rankings
