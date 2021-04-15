from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.category import Category
from app.models.product import ProductType


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    product_condition: Optional[str]
    categories: Optional[List[str]]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    sold: Optional[bool]


class Product(ProductBase):
    id: Optional[int]
    categories: Optional[List[Category]]
    sold: bool
    product_type: ProductType

    class Config:
        orm_mode = True
