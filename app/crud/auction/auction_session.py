from typing import List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from fastapi.encoders import  jsonable_encoder

from app.models.auction import Bid, AuctionState, BID_INCREASE_AMOUNT
from app.crud.auction.bid import bid as crud_bid
from app.models.auction import AuctionSession
from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, BidCreate
from app.crud.base import CRUDBase


class CRUDAuctionSession(CRUDBase[AuctionSession, AuctionSessionCreate, AuctionSessionUpdate]):

    def create_with_ending_date(self, db: Session, obj_in: AuctionSessionCreate, ending_at: datetime) -> AuctionSession:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, ending_at=ending_at)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def check_if_auction_ended(db: Session, db_obj: AuctionSession) -> AuctionSession:
        if db_obj.ending_at and db_obj.ending_at < datetime.now():
            db_obj.auction_state = AuctionState.ENDED
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> AuctionSession:
        db_obj = db.query(self.model).options(
            selectinload(self.model.auction)
        ).get(id)
        db_obj = CRUDAuctionSession.check_if_auction_ended(db, db_obj)
        return db_obj

    def bid_in_auction(
        self,
        db: Session,
        id: int,
        bid_amount: float,
        bidder_id: int
    ) -> Bid:

        current_auction_session = self.get(db=db, id=id)

        # if first bid in auction then set auction_state from created to ongoing
        if current_auction_session.auction_state == AuctionState.CREATED.value:
            current_auction_session.auction_state = AuctionState.ONGOING

        bid_obj = BidCreate(bid_amount=bid_amount)
        bid_db = crud_bid.create_with_owner(
            db=db, obj_in=bid_obj, usr_id=bidder_id)

        current_auction_session.minimum_bid_amount = \
            current_auction_session.minimum_bid_amount + BID_INCREASE_AMOUNT

        current_auction_session.bids.append(bid_db)
        current_auction_session.last_bid_at = bid_db.created_at

        winning_bid = crud_bid.get(db, id=current_auction_session.winning_bid_id)
        if winning_bid is None or bid_db.bid_amount > winning_bid.bid_amount:
            current_auction_session.winning_bid_id = bid_db.id
        db.add(current_auction_session)
        db.commit()
        db.refresh(current_auction_session)
        return bid_db

    def get_bids(
            self,
            db: Session,
            id: int,
    ) -> List[Bid]:
        # TODO: filter by auction_session_id
        auction_session = self.get(db, id=id)
        return auction_session.bids


auction_session = CRUDAuctionSession(AuctionSession)
