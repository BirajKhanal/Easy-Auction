from typing import List
from sqlalchemy.orm import Session

from app.models.auction import AuctionSession
from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate
from app.crud.base import CRUDBase


class CRUDAuctionSession(CRUDBase[AuctionSession, AuctionSessionCreate, AuctionSessionUpdate]):
    pass


auction_session = CRUDAuctionSession(AuctionSession)
