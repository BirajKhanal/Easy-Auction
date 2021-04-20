from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.models.auction import Bid
from app.crud.auction.bid import bid as crud_bid
from app.models.auction import AuctionSession
from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, BidCreate
from app.crud.base import CRUDBase


class CRUDAuctionSession(CRUDBase[AuctionSession, AuctionSessionCreate, AuctionSessionUpdate]):
    def bid_in_auction_session(
        self,
        db: Session,
        auction_session_id: int,
        bid_amount: float,
        bidder_id: int
    ) -> Bid:
        auction_session = self.get(db=db, id=auction_session_id)
        if not auction_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the specified auction currently does not exists"
            )
        bid_obj = BidCreate(bid_amount=bid_amount)
        bid_db = crud_bid.create_with_owner(
            db=db, obj_in=bid_obj, usr_id=bidder_id)

        # TODO: check auction timelimit and set auction state to END if ended
        # TODO: check minimum bid amount
        # TODO: increase minimum bid amount
        # TODO: logic for winning bid
        # TODO: created_at modified_at
        # TODO: auction state
        # TODO: last bid at

        auction_session.bids.append(bid_db)
        db.add(auction_session)
        db.commit()
        db.refresh(auction_session)
        return bid_db

    def get_bids(
        self,
        db: Session,
        id: int
    ) -> List[Bid]:
        auction_session = self.get(db=db, id=id)
        if not auction_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="the specified auction currently does not exists"
            )
        return auction_session.bids


auction_session = CRUDAuctionSession(AuctionSession)
