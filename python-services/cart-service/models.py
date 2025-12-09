from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class ShoppingCart(SQLModel, table=True):
    __tablename__ = "shopping_cart"

    cart_key: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    asin: str
    time_added: Optional[str] = None
    quantity: int = Field(default=1)
