from typing import List, Optional
from sqlalchemy.orm import Session, join, selectinload
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auctionable
from app.models.product import Product, Category, ProductCondition
from app.schemas.product import ProductCreate
from app.schemas.auction import AuctionableCreate, AuctionableUpdate
from app.crud.base import CRUDBase
from app.crud.product.product import product as crud_product


class CRUDAuctionable(CRUDBase[Auctionable, AuctionableCreate, AuctionableUpdate]):

    def get(self, db: Session, id: int) -> Optional[Auctionable]:
        return db.query(self.model).options(
            selectinload(Auctionable.product)
            .selectinload(Product.inventory)
        ).filter(self.model.id == id).first()

    def create_with_product(
            self,
            db: Session,
            obj_in: AuctionableCreate,
            product_in: ProductCreate,
            categories: List[Category],
            usr_id: int,
            quantity: int
    ) -> Auctionable:

        product_db = crud_product.create_with_owner(
            db=db,
            obj_in=product_in,
            categories=categories,
            usr_id=usr_id,
            quantity=quantity
        )

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, prod_id=product_db.id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


auctionable = CRUDAuctionable(Auctionable)
