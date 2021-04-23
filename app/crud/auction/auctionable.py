from typing import List
from sqlalchemy.orm import Session, join
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auctionable
from app.models.product import Product
from app.schemas.auction import AuctionableCreate, AuctionableUpdate
from app.crud.base import CRUDBase


class CRUDAuctionable(
        CRUDBase[Auctionable, AuctionableCreate, AuctionableUpdate]):
    def create_with_product(
            self,
            db: Session,
            obj_in: AuctionableCreate,
            prod_id: int) -> Auctionable:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, prod_id=prod_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


auctionable = CRUDAuctionable(Auctionable)
