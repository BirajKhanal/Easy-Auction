from typing import List
from sqlalchemy.orm import Session

from app.models.auction import Bid
from app.schemas.auction import BidCreate, BidUpdate
from app.crud.base import CRUDBase


class CRUDBid(CRUDBase[Bid, BidCreate, BidUpdate]):
    pass


bid = CRUDBid(Bid)
