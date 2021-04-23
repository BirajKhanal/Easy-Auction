from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.product import Product
from app.schemas.discount import Discount


class SellableBase(BaseModel):
    price: Optional[float]


class SellableCreate(SellableBase):
    price: float


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: Optional[int]
    product: Product
    discount: Discount

    class Config:
        orm_mode = True


# ShoppingSession schema

class ShoppingSessionBase(BaseModel):
    total: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class ShoppingSessionCreate(ShoppingSessionBase):
    total: int
    created_at: Optional[datetime]


class ShoppingSessionUpdate(ShoppingSessionBase):
    pass


class ShoppingSession(ShoppingSessionBase):
    id: Optional[int]
    user: User

    class Config:
        orm_mode = True
