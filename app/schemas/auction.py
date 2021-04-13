from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AuctionableBase(BaseModel):
    bid_cap: Optional[float]
    starting_bid: Optional[float]
    prod_id: Optional[int]


class AuctionableCreate(AuctionableBase):
    bid_cap: float
    starting_bid: float
    prod_id: int


class Aucitonable(AuctionableBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class AuctionBase(BaseModel):
    duration: Optional[float]
    start_timestamp: Optional[datetime]
    current_bid: Optional[float]
    prod_auc_id: Optional[int]


class AuctionCreate(AuctionBase):
    duration: float
    start_timestamp: datetime
    prod_auc_id: int


class AuctionUpdate(AuctionBase):
    pass


class Auction(AuctionBase):
    id: Optional[int]

    class Config:
        orm_mode = True
