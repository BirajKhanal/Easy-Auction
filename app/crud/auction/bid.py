from typing import List
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
        db_obj = self.model(**obj_in_data, usr_id=usr_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


bid = CRUDBid(Bid)
