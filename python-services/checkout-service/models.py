from typing import Optional
from sqlmodel import Field, SQLModel

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: str = Field(primary_key=True)
    user_id: int
    order_details: str
    order_time: str
    order_total: float

class ProductInventory(SQLModel, table=True):
    __tablename__ = "product_inventory"

    asin: str = Field(primary_key=True)
    quantity: int
