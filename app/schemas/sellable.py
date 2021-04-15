from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.product import Product


class SellableBase(BaseModel):
    price: Optional[float]
    discount: Optional[float]


class SellableCreate(SellableBase):
    price: float


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: Optional[int]
    product: Product

    class Config:
        orm_mode = True
