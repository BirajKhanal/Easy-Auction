from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.models.auction import Bid, Auction
from app.crud.auction.bid import bid as crud_bid
from app.models.auction import AuctionSession
from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, BidCreate
from app.crud.base import CRUDBase


class CRUDAuctionSession(CRUDBase[AuctionSession, AuctionSessionCreate, AuctionSessionUpdate]):

    def bid_in_auction(
        self,
        db: Session,
        id: int,
        bid_amount: float,
        bidder_id: int
    ) -> Bid:

        bid_obj = BidCreate(bid_amount=bid_amount)
        bid_db = crud_bid.create_with_owner(
            db=db, obj_in=bid_obj, usr_id=bidder_id)

        #   auction_state = ['STARTED', 'ENDED', 'CANCELED', 'ONGOING']
        # TODO: set auction_winner to winning_bid.usr_id if time >= ending_at
        # TODO: set auction state to ENDED if time >= ending_at
        # TODO: check auction timelimit and set auction state to ONGOING if still in timelimit and auction_state = 'STARTED'
        # TODO: check minimum bid amount raise exception if bid < minimum_bid_amount
        # TODO: increase minimum bid amount
        # TODO: check if the current bid is winner and update winning_bid
        # TODO: update created_at of bid
        # TODO: update last_bid_at of auction_session

        auction_session = self.get(db=db, id=id)

        auction_session.bids.append(bid_db)
        db.add(auction_session)
        db.commit()
        db.refresh(auction_session)
        return bid_db


auction_session = CRUDAuctionSession(AuctionSession)
