from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User


class SellableBase(BaseModel):
    price: Optional[float]
    # TODO: Discount should have its own schema
    # discount: Optional[float]


class SellableCreate(SellableBase):
    price: float


class SellableUpdate(SellableBase):
    pass


class Sellable(SellableBase):
    id: Optional[int]

    class Config:
        orm_mode = True
