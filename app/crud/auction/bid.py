from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.auction import Bid
from app.schemas.auction import BidCreate, BidUpdate
from app.crud.base import CRUDBase


class CRUDBid(CRUDBase[Bid, BidCreate, BidUpdate]):
    def create_with_owner(
        self,
        db: Session,
        obj_in: BidCreate,
        usr_id: int
    ) -> Bid:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, created_at=datetime.now(), usr_id=usr_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_auction(
        self,
        db: Session,
        auction_session_id: int,
        skip: int = 0,
        limit: int = 1000
    ) -> List[Bid]:
        # TODO: filter by auction_session_id
        return db.query(self.model).offset(skip).limit(limit).all()


bid = CRUDBid(Bid)
