from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.sellable import Sellable


class CartBase(BaseModel):
    quantity: Optional[int]
    sellables: Optional[List[Sellable]]


class CartCreate(CartBase):


class CartUpdate(CartBase):
    pass


class CartInDB(CartBase):
    id: Optional[int]

    class Config:
        orm_mode = True
