from typing import List
from sqlalchemy.orm import Session

from app.models.sell import Cart
from app.schemas.cart import CartCreate, CartUpdate
from app.crud.base import CRUDBase


class CRUDCart(CRUDBase[Cart, CartCreate, CartUpdate]):
    pass


cart = CRUDCart(Cart)
