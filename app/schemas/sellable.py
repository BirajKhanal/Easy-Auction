from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User


class SellableBase(BaseModel):
    price: Optional[float]


class SellableCreate(SellableBase):
    price: float


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: int

    class Config:
        orm_mode = True


# ShoppingSession schema

class ShoppingSessionBase(BaseModel):
    total: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class ShoppingSessionCreate(ShoppingSessionBase):
    pass


class ShoppingSessionUpdate(ShoppingSessionBase):
    pass


class ShoppingSession(ShoppingSessionBase):
    class Config:
        orm_mode = True


# Discount shchema


class DiscountBase(BaseModel):
    pass


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(DiscountBase):
    pass


class Discount(DiscountBase):
    class Config:
        orm_mode = True
