from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from fastapi.encoders import jsonable_encoder

from app.models.auction import Bid, AuctionState, BID_INCREASE_AMOUNT
from app.crud.auction.bid import bid as crud_bid
from app.crud.auction.auction import auction as crud_auction
from app.models.auction import AuctionSession
from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, BidCreate
from app.crud.base import CRUDBase


def is_auction_ended(db_obj: AuctionSession) -> bool:
    if db_obj.ending_at and db_obj.ending_at < datetime.now():
        return True
    return False


class CRUDAuctionSession(CRUDBase[AuctionSession, AuctionSessionCreate, AuctionSessionUpdate]):

    @staticmethod
    def update_auction_state(db: Session, db_obj: AuctionSession, state: AuctionState, commit=True) -> AuctionSession:
        winning_bid = crud_bid.get(
            db, id=db_obj.winning_bid_id)
        if winning_bid:
            db_obj.auction.auction_winner_id = winning_bid.usr_id
        db_obj.auction_state = state
        if commit:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def create_with_ending_date(self, db: Session, obj_in: AuctionSessionCreate, ending_at: datetime) -> AuctionSession:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, ending_at=ending_at)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    """
    gets aution table along with auction_session table
    updates the auction state
    """

    def get(self, db: Session, id: int) -> AuctionSession:
        db_obj = db.query(self.model).options(
            selectinload(self.model.auction)
        ).get(id)

        # TODO: this should be done by some scheduler
        if is_auction_ended(db_obj) and db_obj.auction_state not in [AuctionState.CANCELED, AuctionState.ENDED]:
            db_obj = self.update_auction_state(db, db_obj, AuctionState.ENDED)
        return db_obj

    """
    Add new Bid to the AuctionSession
    Update AuctionState from CREATED To ONGOING
    Update minimum_bid_amount
    Update winninb_bid
    """

    def add_new_bid(self, db: Session, db_obj: AuctionSession, bid_db: Bid) -> Bid:
        if db_obj.auction_state == AuctionState.CREATED:
            db_obj.auction_state = AuctionState.ONGOING

        db_obj.minimum_bid_amount = bid_db.bid_amount + BID_INCREASE_AMOUNT
        db_obj.bids.append(bid_db)
        db_obj.last_bid_at = bid_db.created_at

        w_b = db_obj.winning_bid
        if not w_b or bid_db.bid_amount > w_b.bid_amount:
            db_obj.winning_bid = bid_db

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return bid_db

    # def get_bids(
    #         self,
    #         db: Session,
    #         id: int,
    # ) -> List[Bid]:
    #     auction_session = self.get(db, id=id)
    #     return auction_session.bids


auction_session = CRUDAuctionSession(AuctionSession)
