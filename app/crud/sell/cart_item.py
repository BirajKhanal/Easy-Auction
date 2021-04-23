from typing import List
from sqlalchemy.orm import Session

from app.models.sell import CartItem
from app.schemas.cart import CartItemCreate, CartItemUpdate
from app.crud.base import CRUDBase


class CRUDCartItem(CRUDBase[CartItem, CartItemCreate, CartItemUpdate]):
    pass


cart_item = CRUDCartItem(CartItem)
