from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User


class SellableBase(BaseModel):
    price: Optional[float]
    discount: Optional[float]
    quantity: Optional[int]
    prod_id: Optional[int]


class SellableCreate(SellableBase):
    price: float
    prod_id: int


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: Optional[int]

    class Config:
        orm_mode = True
