from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload, raiseload
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auction, Auctionable, AuctionState
from app.models.product import Product, ProductCondition
from app.schemas.auction import AuctionCreate, AuctionUpdate, AuctionableCreate, AuctionSessionCreate
from app.schemas.product import ProductCreate
from app.crud.base import CRUDBase
from app.crud.product import (
    product as crud_product,
    category as crud_category
)
from app.crud.auction.auctionable import auctionable as crud_auctionable
from app.crud.auction.auction_session import auction_session as crud_auction_session
from app.crud.auction.bid import bid as crud_bid


class CRUDAuction(CRUDBase[Auction, AuctionCreate, AuctionUpdate]):

    # TODO: use selectinload
    def get_complete(self, db: Session, id: int) -> Auction:
        query = db.query(self.model).options(
            selectinload(Auction.auctionable)
            .selectinload(Auctionable.product)
            .selectinload(Product.inventory),
            selectinload(Auction.auctionable)
            .selectinload(Auctionable.product)
            .selectinload(Product.categories),
            selectinload(Auction.auction_session),
            raiseload('*')
        )
        db_obj = query.get(id)
        db_obj = CRUDAuction.check_if_auction_ended(db=db, db_obj=db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Auction:
        query = db.query(self.model).options(
            selectinload(Auction.auctionable)
        )
        db_obj = query.get(id)
        db_obj = CRUDAuction.check_if_auction_ended(db=db, db_obj=db_obj)
        return db_obj

    @staticmethod
    def check_if_auction_ended(db: Session, db_obj: Auction) -> Auction:
        if db_obj.auction_session.ending_at < datetime.now():
            winning_bid = crud_bid.get(db, id=db_obj.auction_session.winning_bid_id)
            if winning_bid:
                db_obj.auction_winner_id = winning_bid.usr_id
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    # TODO: use selectinload
    def get_multi(self, db: Session, skip: int = 0, limit: int = 1000):
        query = db.query(self.model).options(
            selectinload(Auction.auctionable)
            .selectinload(Auctionable.product)
            .selectinload(Product.inventory),
            selectinload(Auction.auctionable)
            .selectinload(Auctionable.product)
            .selectinload(Product.categories),
            raiseload('*')
        )
        return query.offset(skip).limit(limit).all()

    def get_multi_by_owner(
            self, db: Session, *, usr_id: int, skip: int = 0, limit: int = 100
    ) -> List[Auction]:
        # TODO: optimize the query beceause this is nested schema
        return db.query(
            self.model).filter(
            self.model.owner_id == usr_id).offset(skip).limit(limit).all()


    def create_with_auctionable_and_session(
        self,
        db: Session,
        obj_in: AuctionCreate,
        owner_id: int,
        auctionable_id: int,
        auction_session_id: int
    ) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            owner_id=owner_id,
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
        # TODO: need to optimise this part and this is too ugly
        # create a product
        categories = crud_category.get_multi_by_ids(
            db=db, category_ids=categories)
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

        # create an auctionable
        auctionable_obj = AuctionableCreate(
            bid_cap=bid_cap,
            starting_bid=starting_bid,
        )
        auctionable_db = crud_auctionable.create_with_product(
            db=db,
            obj_in=auctionable_obj,
            prod_id=product_db.id,
        )

        # create an auction_session

        auction_session_obj = AuctionSessionCreate(
            minimum_bid_amount=starting_bid,
            auction_state=AuctionState.CREATED
        )
        auction_session_db = crud_auction_session.create_with_ending_date(
            db=db,
            obj_in=auction_session_obj,
            ending_at=ending_at
        )

        # create an auction
        auction_obj = AuctionCreate(
            name=name,
        )
        auction_db = self.create_with_auctionable_and_session(
            db=db,
            obj_in=auction_obj,
            owner_id=usr_id,
            auctionable_id=auctionable_db.id,
            auction_session_id=auction_session_db.id
        )

        return auction_db


auction = CRUDAuction(Auction)
