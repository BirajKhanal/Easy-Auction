from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    product_condition: Optional[str]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: Optional[int]

    class Config:
        orm_mode = True
