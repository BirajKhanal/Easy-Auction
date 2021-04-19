from typing import List
from sqlalchemy.orm import Session

from app.models.sell import ShoppingSession
from app.schemas.sellable import ShoppingSessionCreate, ShoppingSessionUpdate
from app.crud.base import CRUDBase


class CRUDShoppingSession(CRUDBase[ShoppingSession, ShoppingSessionCreate, ShoppingSessionUpdate]):
    pass


shopping_session = CRUDShoppingSession(ShoppingSession)
