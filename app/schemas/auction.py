from typing import Optional
from datetime import datetime
from pydantic import BaseModel


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

    class Config:
        orm_mode = True


# auction schemas

class AuctionBase(BaseModel):
    duration: Optional[float]
    start_timestamp: Optional[datetime]
    current_bid: Optional[float]


class AuctionCreate(AuctionBase):
    duration: float
    start_timestamp: datetime


class AuctionUpdate(AuctionBase):
    pass


class Auction(AuctionBase):
    id: Optional[int]
    auctionable: Auctionable

    class Config:
        orm_mode = True


# auction session schemas

class AuctionSessionBase(BaseModel):
    pass


class AuctionSessionCreate(AuctionSessionBase):
    pass


class AuctionSessionUpdate(AuctionSessionBase):
    pass


class AuctionSession(AuctionSessionBase):
    class Config:
        orm_mode = True


# bid schemas

class BidBase(BaseModel):
    pass


class BidCreate(BidBase):
    pass


class BidUpdate(BidBase):
    pass


class Bid(BidBase):
    class Config:
        orm_mode = True
