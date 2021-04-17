from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.product import Product, ProductType
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate
from app.crud.base import CRUDBase
from app import crud


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(
        self,
        db: Session,
        obj_in: ProductCreate,
        usr_id: int,
        product_type: ProductType,
        quantity: int
    ) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data.get('categories', None):
            prod_categories = crud.category.get_multi_categories(
                db, categories=obj_in_data['categories'])
            obj_in_data["categories"] = prod_categories
        else:
            del obj_in_data['categories']
        # TODO: set inventory quantity default to 1 or value of quantity: int
        inventory_obj = InventoryCreate(
            quantity=quantity)
        inventory = crud.inventory.create(
            db=db, obj_in=inventory_obj, restocked_at=datetime.now())
        db_obj = self.model(
            **obj_in_data,
            usr_id=usr_id,
            product_type=product_type,
            inventory=inventory,
            created_at=datetime.now(),
            modified_at=datetime.now()
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

    def buy_product(self, db: Session, db_obj: Product, buyer: User) -> Product:
        db_obj.sold = True
        # TODO: Do something to tell who bought the item maybe another table?
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)
