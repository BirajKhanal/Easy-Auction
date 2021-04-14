from typing import List
from sqlalchemy.orm import Session

from app.models.sell import Sellable
from app.schemas.sellable import SellableCreate, SellableUpdate
from app.crud.base import CRUDBase


class CRUDSellable(CRUDBase[Sellable, SellableCreate, SellableUpdate]):
    pass


sellable = CRUDSellable(Sellable)
