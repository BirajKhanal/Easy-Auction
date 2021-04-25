from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload, raiseload
from fastapi.encoders import jsonable_encoder

from app.models.auction import Auction, Auctionable, AuctionState
from app.models.product import Product, ProductCondition, Category
from app.schemas.auction import AuctionCreate, AuctionUpdate, AuctionableCreate, AuctionSessionCreate
from app.schemas.product import ProductCreate
from app.crud.base import CRUDBase
from app.crud.auction.bid import bid as crud_bid


class CRUDAuction(CRUDBase[Auction, AuctionCreate, AuctionUpdate]):

    @staticmethod
    def check_if_auction_ended(db_obj: Auction) -> bool:
        if db_obj and db_obj.auction_session.ending_at < datetime.now():
            return True
        return False

    @staticmethod
    def update_auction_winner(db: Session, db_obj: Auction, commit=True) -> Auction:
        winning_bid = crud_bid.get(
            db, id=db_obj.auction_session.winning_bid_id)
        if winning_bid:
            db_obj.auction_winner_id = winning_bid.usr_id
        db_obj.auction_session.auction_state = AuctionState.ENDED
        if commit:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

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

        if self.check_if_auction_ended(db_obj=db_obj):
            db_obj = self.update_auction_winner(db, db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Auction:
        query = db.query(self.model).options(
            selectinload(Auction.auctionable)
        )
        db_obj = query.get(id)
        if self.check_if_auction_ended(db_obj=db_obj) and not db_obj.auction_winner_id:
            db_obj = self.update_auction_winner(db, db_obj)
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
            selectinload(Auction.auction_session),
            raiseload('*')
        )
        return query.offset(skip).limit(limit).all()

    def get_multi_by_owner(
            self, db: Session, *, usr_id: int, skip: int = 0, limit: int = 100
    ) -> List[Auction]:
        return db.query(
            self.model).options(
            selectinload(Auction.auctionable)
                .selectinload(Auctionable.product)
                .selectinload(Product.inventory),
            selectinload(Auction.auctionable)
                .selectinload(Auctionable.product)
                .selectinload(Product.categories),
            selectinload(Auction.auction_session),
            raiseload('*')
        ).filter(
            self.model.owner_id == usr_id).offset(skip).limit(limit).all()


auction = CRUDAuction(Auction)
