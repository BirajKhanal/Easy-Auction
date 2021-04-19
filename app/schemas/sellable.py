from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User


class SellableBase(BaseModel):
    price: Optional[float]


class SellableCreate(SellableBase):
    price: float


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: Optional[int]

    class Config:
        orm_mode = True

# CartItem schema


class CartItemBase(BaseModel):
    pass


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    pass


class CartItem(CartItemBase):
    class Config:
        orm_mode = True


# ShoppingSession schema

class ShoppingSessionBase(BaseModel):
    pass


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
