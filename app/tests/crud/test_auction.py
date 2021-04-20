from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from random import randint

from app.crud.auction import (
    auction as crud_auction,
    auction_session as crud_auction_session,
    auctionable as crud_auctionable
)
from app.crud.product import product as crud_product
from app.schemas import auction
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_int, random_float
from app.tests.utils.product import create_random_category, random_product_condition
from app.tests.utils.auction import create_random_auction


def test_create_with_owner(
    db: Session,
) -> None:
    name = random_lower_string()
    description = random_lower_string()
    cat1 = create_random_category(db)
    cat2 = create_random_category(db)
    cat3 = create_random_category(db)
    categories = [cat1.id, cat2.id, cat3.id]
    product_condition = random_product_condition()
    quantity = random_int()
    bid_cap = random_float()
    starting_bid = random_float()
    ending_at = datetime.now()
    user = create_random_user(db)

    auction = crud_auction.create_with_owner(
        db=db,
        name=name,
        description=description,
        categories=categories,
        product_condition=product_condition,
        quantity=quantity,
        bid_cap=bid_cap,
        starting_bid=starting_bid,
        ending_at=ending_at,
        usr_id=user.id
    )

    assert auction

    auctionable = crud_auctionable.get(db=db, id=auction.auctionable_id)
    assert auctionable

    auction_session = crud_auction_session.get(
        db=db, id=auction.auction_session_id)
    assert auction_session

    product = crud_product.get(db=db, id=auctionable.prod_id)
    assert product

    categories_in_db = product.categories
    assert categories_in_db[0].id == cat1.id
    assert categories_in_db[1].id == cat2.id
    assert categories_in_db[2].id == cat3.id


def test_update_auction(
    db: Session
):
    auction = create_random_auction(db=db)


def test_get_single_auction(
    db: Session
):
    auction = create_random_auction(db=db)
    auction_in_db = crud_auction.get(db=db, id=auction.id)

    assert auction_in_db


def test_bid_in_auction(
    db: Session
):
    auction = create_random_auction(db)
    bidder = create_random_user(db)
    bid_amount = random_int()

    bid = crud_auction_session.bid_in_auction_session(
        db=db,
        auction_session_id=auction.auction_session_id,
        bid_amount=bid_amount,
        bidder_id=bidder.id
    )

    bids_in_db = crud_auction_session.get_bids(
        db=db,
        id=auction.auction_session_id
    )

    assert bids_in_db
    assert bids_in_db[0].id == bid.id
    assert bids_in_db[0].usr_id == bidder.id
