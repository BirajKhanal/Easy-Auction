from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.product import Product
from app.models.user import User
from app.models.auction import Auctionable
from app.models.sell import Sellable
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate
from app.schemas.auction import AuctionableCreate
from app.schemas.sellable import SellableCreate
from app.crud.base import CRUDBase
from app import crud


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(
        self,
        db: Session,
        obj_in: ProductCreate,
        usr_id: int,
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, usr_id=usr_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def get_multi_by_owner(
        self, db: Session, *, usr_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
            .filter(Product.usr_id == usr_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


product = CRUDProduct(Product)
