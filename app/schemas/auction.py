from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.schemas.product import Product


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
