from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.sellable import Sellable


class CartItemBase(BaseModel):
    quantity: Optional[int]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class CartItemCreate(CartItemBase):
    quantity: int
    sellable_id: int
    created_at: datetime
    session_id: int


class CartItemUpdate(CartItemBase):
    pass


class Cart(CartItemBase):
    id: Optional[int]
    sellable: Sellable

    class Config:
        orm_mode = True


class CartLogBase(BaseModel):
    quantity: Optional[int]
    created_at: Optional[int]


class CartLogCreate(CartLogBase):
    pass

class CartLogUpdate(CartLogBase):
    pass

class CartLog(CartLogBase):
    id: Optional[int]

    class Config:
        orm_mode = True
