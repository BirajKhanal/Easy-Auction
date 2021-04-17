from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from app.schemas.category import Category
from app.schemas.sellable import SellableBase
from app.schemas.auction import AuctionableBase
from app.models.product import ProductType


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
    product_condition: Optional[str]
    categories: Optional[List[str]]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    sold: Optional[bool]


class Product(ProductBase):
    id: Optional[int]
    categories: Optional[List[Category]]
    product_type: ProductType
    inventory: Optional[Inventory]

    class Config:
        orm_mode = True


class ProductCreateRequest(ProductCreate):
    bid_cap: Optional[float]
    starting_bid: Optional[float]
    price: Optional[float]
    quantity: Optional[int]


class ProductResponse(Product, SellableBase, AuctionableBase):
    pass
