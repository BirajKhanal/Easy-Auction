from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from app.schemas.category import Category
from app.schemas import auction, sellable, category
from app.models.product import ProductCondition


class InventoryBase(BaseModel):
    quantity: Optional[int]


class InventoryCreate(InventoryBase):
    quantity: int


class InventoryUpdate(InventoryBase):
    pass


class Inventory(InventoryBase):
    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    product_condition: Optional[ProductCondition]
    categories: Optional[List[category.CategoryBase]]
    inventory: Optional[InventoryBase]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: Optional[int]
    categories: Optional[List[Category]]
    inventory: Optional[Inventory]

    class Config:
        orm_mode = True
