from typing import List, Optional, Set
from sqlmodel import Field, SQLModel, JSON
from sqlalchemy import Column
from decimal import Decimal

# Using JSON for collection types since Yugabyte/Postgres supports it naturally 
# and SQLModel/SQLAlchemy can map it.

class ProductMetadata(SQLModel, table=True):
    __tablename__ = "products"
    
    id: str = Field(primary_key=True, alias="asin")
    brand: Optional[str] = None
    categories: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    imUrl: Optional[str] = Field(sa_column_kwargs={"name": "imurl"})
    price: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None
    also_bought: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    also_viewed: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    bought_together: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    buy_after_viewing: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    num_reviews: Optional[int] = None
    num_stars: Optional[float] = None
    avg_stars: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True

class ProductRanking(SQLModel, table=True):
    __tablename__ = "product_rankings"
    
    # Composite primary key in Cassandra/Yugabyte usually. 
    # Since SQLModel doesn't support composite PKs neatly in the class definition params,
    # we'll model it assuming we can query by fields.
    # Note: The original Java code used a composite key class 'ProductRankingKey'.
    
    asin: str = Field(primary_key=True)
    category: str = Field(primary_key=True)
    sales_rank: int
    title: Optional[str] = None
    price: Optional[float] = None
    imUrl: Optional[str] = Field(sa_column_kwargs={"name": "imurl"})
    num_reviews: Optional[int] = None
    num_stars: Optional[float] = None
    avg_stars: Optional[float] = None
