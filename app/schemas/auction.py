from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.product import Product
from app.models.auction import AuctionState


# auctionalbe schemas

class AuctionableBase(BaseModel):
    bid_cap: Optional[float]
    starting_bid: Optional[float]


class AuctionableCreate(AuctionableBase):
    bid_cap: float
    starting_bid: float


class AuctionableUpdate(AuctionableBase):
    pass


class Auctionable(AuctionableBase):
    id: Optional[int]
    product: Product

    class Config:
        orm_mode = True


# auction session schemas

class AuctionSessionBase(BaseModel):
    minimum_bid_amount: Optional[float]
    auction_state: Optional[AuctionState]


class AuctionSessionCreate(AuctionSessionBase):
    minimum_bid_amount: float
    auction_state: AuctionState = AuctionState.CREATED



class AuctionSessionUpdate(AuctionSessionBase):
    winning_bid: int


class AuctionSession(AuctionSessionBase):
    ending_at: Optional[datetime]
    class Config:
        orm_mode = True


# bid schemas

class BidBase(BaseModel):
    bid_amount: Optional[float]


class BidCreate(BidBase):
    bid_amount: float


class BidUpdate(BidBase):
    pass


class Bid(BidBase):
    id: int
    usr_id: int

    class Config:
        orm_mode = True

# auction schemas


class AuctionBase(BaseModel):
    name: Optional[str]


class AuctionCreate(AuctionBase):
    pass


class AuctionUpdate(AuctionBase):
    pass


class Auction(AuctionBase):
    id: Optional[int]
    auctionable: Auctionable
    auction_session: AuctionSession

    class Config:
        orm_mode = True
