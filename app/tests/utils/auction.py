from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.crud.auction import (
    auction as crud_auction,
)
from app.models.auction import Auction, Bid, AuctionState
from app.models.user import User
from app.schemas.auction import AuctionSessionCreate, AuctionCreate, AuctionableCreate, BidCreate
from app.schemas.product import ProductCreate
from app.crud.auction.auctionable import auctionable as crud_auctionable
from app.crud.auction.auction_session import auction_session as crud_auction_session
from app.crud.auction.bid import bid as crud_bid
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_int, random_float
from app.tests.utils.product import create_random_category, random_product_condition


def create_random_auction(
        db: Session,
        bid_cap: float = 0,
        user: User = None,
        ending_at: datetime = None
) -> Auction:
    name = random_lower_string()
    description = random_lower_string()
    cat1 = create_random_category(db)
    cat2 = create_random_category(db)
    cat3 = create_random_category(db)
    categories = [cat1, cat2, cat3]
    product_condition = random_product_condition()
    if not bid_cap:
        bid_cap = random_float()
    quantity = random_int()
    starting_bid = random_float()
    if not ending_at:
        ending_at = datetime.now() + timedelta(days=1)
    if not user:
        user = create_random_user(db)

    product_obj = ProductCreate(
        name=name,
        description=description,
        product_condition=product_condition
    )

    auctionable_obj = AuctionableCreate(
        bid_cap=bid_cap,
        starting_bid=starting_bid,
    )

    auctionable_db = crud_auctionable.create_with_product(
        db=db,
        obj_in=auctionable_obj,
        product_in=product_obj,
        categories=categories,
        usr_id=user.id,
        quantity=quantity
    )

    auction_session_obj = AuctionSessionCreate(
        minimum_bid_amount=starting_bid,
        auction_state=AuctionState.CREATED
    )

    auction_session_db = crud_auction_session.create_with_ending_date(
        db=db,
        obj_in=auction_session_obj,
        ending_at=ending_at
    )

    auction_obj = AuctionCreate(
        name=name,
        auctionable_id=auctionable_db.id,
        auction_session_id=auction_session_db.id,
        owner_id=user.id
    )

    auction_db = crud_auction.create(db, obj_in=auction_obj)

    return auction_db


def create_random_bid(db: Session, minimum_bid_amount: float) -> Bid:
    user = create_random_user(db)
    bid_amount = minimum_bid_amount + random_float()
    bid_obj = BidCreate(bid_amount=bid_amount, usr_id=user.id)
    return crud_bid.create(db, obj_in=bid_obj)
