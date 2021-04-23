from typing import List
from sqlalchemy.orm import Session

from app.models.sell import CartLog
from app.schemas.cart import CartLogCreate, CartLogUpdate
from app.crud.base import CRUDBase


class CRUDCartLog(CRUDBase[CartLog, CartLogCreate, CartLogUpdate]):
    pass


cart_item = CRUDCartLog(CartLog)

