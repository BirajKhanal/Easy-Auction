from typing import List
from sqlalchemy.orm import Session

from app.models.sell import Discount
from app.schemas.sellable import DiscountCreate, DiscountUpdate
from app.crud.base import CRUDBase


class CRUDDiscount(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
    pass


discount = CRUDDiscount(Discount)
