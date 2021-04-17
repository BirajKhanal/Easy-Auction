from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.sellable import Sellable


class CartBase(BaseModel):
    sellables: Optional[List[Sellable]]
    owner: Optional[User]


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class Cart(CartBase):
    id: Optional[int]

    class Config:
        orm_mode = True
