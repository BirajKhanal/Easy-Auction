from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.category import Category


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    product_condition: Optional[str]
    categories: Optional[List[str]]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: Optional[int]
    categories: Optional[List[Category]]

    class Config:
        orm_mode = True
