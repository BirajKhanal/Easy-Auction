from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.product import Product, ProductType
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud.base import CRUDBase
from app.crud import crud_category


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(self, db: Session, obj_in: ProductCreate, usr_id: int, product_type: ProductType) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in.categories:
            prod_categories = crud_category.category.get_multi_categories(
                db, categories=obj_in.categories)
            obj_in_data["categories"] = prod_categories
        else:
            # remove categories from dict before setting in db
            del obj_in_data["categories"]
        db_obj = self.model(**obj_in_data, usr_id=usr_id,
                            product_type=product_type)
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

    def buy_product(self, db: Session, db_obj: Product, buyer: User):
        db_obj.sold = True
        # TODO: Do something to tell who bought the item maybe another table?
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)
