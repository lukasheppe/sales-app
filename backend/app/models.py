import enum
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, DateTime, Enum, Float

from app.database import Base

"""
General models
"""


class ProductType(enum.Enum):
    """
    Enum to represent product types.
    """
    STARTER = 0
    PROFESSIONAL = 1
    ENTERPRISE = 2


"""
Database models
"""


class Sale(Base):
    """
    sqlalchemy ORM object for the sales table
    """
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(Enum(ProductType))
    date = Column(DateTime)
    amount = Column(Float)


class CreateSale(BaseModel):
    """
    Pydantic model of database schema.
    """
    product: ProductType
    created: datetime = Field(default_factory=datetime.utcnow)
    amount: float


"""
API models
"""


class BuyProductRequest(BaseModel):
    """
    Request to buy a specific product.
    """
    product_type: ProductType


class BuyProductResponse(BuyProductRequest):
    """
    Response to BuyProductRequest. Contains state, price and date.,
    """
    successful: bool
    price: float
    buy_date: datetime = Field(default_factory=datetime.utcnow)


class SalesOverviewResponse(BaseModel):
    """
    Response model for GET /get_current_money endpoint.
    """
    number_of_sales: int
    volume: float


class DeleteSalesResponse(BaseModel):
    """
    Response model for DELETE /sales endpoint.
    Returns the number of rows deleted.
    """
    num_rows_deleted: int
