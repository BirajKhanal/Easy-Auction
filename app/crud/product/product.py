from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.product import Product, Category
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate
from app.crud.base import CRUDBase
from app.crud.product.inventory import inventory as crud_inventory


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(
        self,
        db: Session,
        obj_in: ProductCreate,
        categories: List[Category],
        usr_id: int,
        quantity: int
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        inventory_obj = InventoryCreate(quantity=quantity)
        inventory_db = crud_inventory.create(
            db=db, obj_in=inventory_obj, restocked_at=datetime.now())
        db_obj = self.model(
            **obj_in_data,
            categories=categories,
            usr_id=usr_id,
            inventory_id=inventory_db.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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
