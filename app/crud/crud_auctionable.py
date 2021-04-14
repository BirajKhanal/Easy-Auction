from typing import List
from sqlalchemy.orm import Session

from app.models.auction import Auctionable
from app.schemas.auction import AuctionableCreate, AuctionableUpdate
from app.crud.base import CRUDBase


class CRUDAuctionable(CRUDBase[Auctionable, AuctionableCreate, AuctionableUpdate]):
    pass


auctionable = CRUDAuctionable(Auctionable)
