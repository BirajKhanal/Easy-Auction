from typing import List
from sqlalchemy.orm import Session, join
from fastapi.encoders import jsonable_encoder

from app.models.sell import Sellable
from app.models.product import Product
from app.models.user import User
from app.schemas.sellable import SellableCreate, SellableUpdate
from app.schemas.product import ProductCreate
from app.crud.base import CRUDBase


class CRUDSellable(CRUDBase[Sellable, SellableCreate, SellableUpdate]):
    def create_with_product(self, db: Session, obj_in: SellableCreate, product_id: int) -> Sellable:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, prod_id=product_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, usr_id: int, skip: int = 0, limit: int = 100
    ) -> List[Sellable]:
        return (
            db.query(self.model)
            .select_from(join(Product, Sellable))
            .filter(Product.usr_id == usr_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


sellable = CRUDSellable(Sellable)
