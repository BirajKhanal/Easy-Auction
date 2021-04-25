from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, join
from fastapi.encoders import jsonable_encoder

from app.models.sell import Sellable
from app.models.product import Product, ProductCondition
from app.models.product import Product

from app.schemas.sellable import SellableCreate, SellableUpdate
from app.schemas.product import ProductCreate
from app.schemas.discount import DiscountCreate, DiscountUpdate

from app.crud.base import CRUDBase
from app.crud.product import(
    product as crud_product,
    category as crud_category
)


class CRUDSellable(CRUDBase[Sellable, SellableCreate, SellableUpdate]):
    def get(self, db: Session, id: int):
        return db.query(Sellable).filter(Sellable.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Sellable).offset(skip).limit(limit).all()

    def create_sellable(
        self,
        db: Session,
        name: str,
        description: str,
        categories: List[int],
        product_condition: ProductCondition,
        quantity: int,
        price: float,
        usr_id: int,
    ) -> Sellable:

        categories = crud_category.get_multi_by_ids(
            db=db,
            category_ids=categories
        )

        product_obj = ProductCreate(
            name=name,
            description=description,
            product_condition=product_condition,
        )

        product_db = crud_product.create_with_owner(
            db=db,
            obj_in=product_obj,
            categories=categories,
            usr_id=usr_id,
            quantity=quantity
        )

        sellable_obj = SellableCreate(
            price=price
        )

        sellable_db = Sellable(
            price=price,
            prod_id=product_db.id,
            discount_id=0
        )

        return db_obj



sellable = CRUDSellable(Sellable)
