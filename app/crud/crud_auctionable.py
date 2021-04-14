from typing import List
from sqlalchemy.orm import Session, join
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auctionable
from app.models.product import Product
from app.schemas.auction import AuctionableCreate, AuctionableUpdate
from app.schemas.product import ProductCreate
from app.crud.base import CRUDBase


class CRUDAuctionable(CRUDBase[Auctionable, AuctionableCreate, AuctionableUpdate]):
    def create_with_product(self, db: Session, obj_in: AuctionableCreate, product: ProductCreate) -> Auctionable:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, product=product)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, usr_id: int, skip: int = 0, limit: int = 100
    ) -> List[Auctionable]:
        return (
            db.query(self.model)
            .select_from(join(Product, Auctionable))
            .filter(Product.usr_id == usr_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


auctionable = CRUDAuctionable(Auctionable)
