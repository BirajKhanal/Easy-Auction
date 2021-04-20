from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, joinedload, raiseload, contains_eager, Load
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auction, Auctionable
from app.models.product import Product, Category
from app.schemas.auction import AuctionCreate, AuctionUpdate
from app.crud.base import CRUDBase
from app.models.product import ProductCondition
from app.schemas import (
    product as schema_product,
    auction as schema_auction
)
from app.crud.product import (
    product as crud_product,
    category as crud_category
)
from app.crud.auction.auctionable import auctionable as crud_auctionable
from app.crud.auction.auction_session import auction_session as crud_auction_session


class CRUDAuction(CRUDBase[Auction, AuctionCreate, AuctionUpdate]):

    def get(self, db: Session, id: int):
        query = db.query(self.model).options(
            joinedload(Auction.auctionable, innerjoin=True)
            .joinedload(Auctionable.product, innerjoin=True)
            .joinedload(Product.inventory, innerjoin=True),
            joinedload(Auction.auctionable, innerjoin=True)
            .joinedload(Auctionable.product, innerjoin=True)
            .joinedload(Product.categories, innerjoin=True),
            Load(self.model).raiseload('*')
        )

        return query.filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 1000):
        query = db.query(self.model).options(
            joinedload(Auction.auctionable, innerjoin=True)
            .joinedload(Auctionable.product, innerjoin=True)
            .joinedload(Product.inventory, innerjoin=True),
            joinedload(Auction.auctionable, innerjoin=True)
            .joinedload(Auctionable.product, innerjoin=True)
            .joinedload(Product.categories, innerjoin=True),
            Load(self.model).raiseload('*')
        )
        return query.offset(skip).limit(limit).all()

    def create_with_auctionable_and_session(
        self,
        db: Session,
        obj_in: AuctionCreate,
        ending_at: datetime,
        auctionable_id: int,
        auction_session_id: int
    ) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            created_at=datetime.now(),
            ending_at=ending_at,
            auctionable_id=auctionable_id,
            auction_session_id=auction_session_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_owner(
        self,
        db: Session,
        name: str,
        description: str,
        categories: List[int],
        product_condition: ProductCondition,
        quantity: int,
        bid_cap: float,
        starting_bid: float,
        ending_at: datetime,
        usr_id: int
    ) -> Auction:
        # create a product
        categories = crud_category.get_multi_by_ids(
            db=db, category_ids=categories)
        product_obj = schema_product.ProductCreate(
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

        # create an auctionable
        auctionable_obj = schema_auction.AuctionableCreate(
            bid_cap=bid_cap,
            starting_bid=starting_bid,
        )
        auctionable_db = crud_auctionable.create_with_product(
            db=db,
            obj_in=auctionable_obj,
            prod_id=product_db.id,
        )

        # create an auction_session
        auction_session_obj = schema_auction.AuctionSessionCreate(
            minimum_bid_amount=starting_bid,
        )
        auction_session_db = crud_auction_session.create(
            db=db,
            obj_in=auction_session_obj
        )

        # create an auction
        auction_obj = schema_auction.AuctionCreate(
            name=name,
        )
        auction_db = self.create_with_auctionable_and_session(
            db=db,
            obj_in=auction_obj,
            ending_at=ending_at,
            auctionable_id=auctionable_db.id,
            auction_session_id=auction_session_db.id
        )

        return auction_db


auction = CRUDAuction(Auction)
