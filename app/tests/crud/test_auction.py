import time
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.auction import AuctionState
from app.schemas.product import ProductCreate
from app.schemas.auction import AuctionCreate, AuctionableCreate, AuctionSessionCreate
from app.crud.auction import (
    auction as crud_auction,
    auction_session as crud_auction_session,
    auctionable as crud_auctionable
)
from app.crud.product import product as crud_product
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_int, random_float
from app.tests.utils.product import create_random_category, random_product_condition
from app.tests.utils.auction import create_random_auction, create_random_bid


def test_create_with_owner(
    db: Session,
) -> None:
    name = random_lower_string()
    description = random_lower_string()
    cat1 = create_random_category(db)
    cat2 = create_random_category(db)
    cat3 = create_random_category(db)
    categories = [cat1, cat2, cat3]
    product_condition = random_product_condition()
    bid_cap = random_float()
    quantity = random_int()
    starting_bid = random_float()
    ending_at = datetime.now() + timedelta(days=1)
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

    auctionable = crud_auctionable.create_with_product(
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

    auction_session = crud_auction_session.create_with_ending_date(
        db=db,
        obj_in=auction_session_obj,
        ending_at=ending_at
    )

    auction_obj = AuctionCreate(
        name=name,
        auctionable_id=auctionable.id,
        auction_session_id=auction_session.id,
        owner_id=user.id
    )

    auction = crud_auction.create(db, obj_in=auction_obj)

    assert auction

    assert auctionable

    assert auction_session

    assert auction_session.auction_state == AuctionState.CREATED

    product = crud_product.get(db=db, id=auctionable.prod_id)
    assert product

    categories_in_db = product.categories
    assert categories_in_db[0].id == cat1.id
    assert categories_in_db[1].id == cat2.id
    assert categories_in_db[2].id == cat3.id


def test_update_auction(
    db: Session
):
    pass


def test_get_single_auction(
    db: Session
):
    auction = create_random_auction(db=db)
    auction_in_db = crud_auction.get(db=db, id=auction.id)

    assert auction_in_db
    assert auction.auctionable_id == auction_in_db.auctionable_id
    assert auction.auction_session_id == auction_in_db.auction_session_id


def test_add_new_bid(
    db: Session
):
    auction = create_random_auction(db)
    bid1 = create_random_bid(db, auction.auction_session.minimum_bid_amount)
    bid2 = create_random_bid(db, minimum_bid_amount=bid1.bid_amount)
    bid3 = create_random_bid(db, minimum_bid_amount=bid2.bid_amount)

    crud_auction_session.add_new_bid(db, auction.auction_session, bid1)
    crud_auction_session.add_new_bid(db, auction.auction_session, bid2)
    crud_auction_session.add_new_bid(db, auction.auction_session, bid3)

    bids_in_db = auction.auction_session.bids

    assert bids_in_db
    assert bids_in_db[0].id == bid1.id
    assert bids_in_db[0].usr_id == bid1.usr_id
    assert bids_in_db[1].id == bid2.id
    assert bids_in_db[1].usr_id == bid2.usr_id
    assert bids_in_db[2].id == bid3.id
    assert bids_in_db[2].usr_id == bid3.usr_id


def test_auction_winner_is_set(
        db: Session
) -> None:
    ending_at = datetime.now() + timedelta(seconds=3)
    auction = create_random_auction(
        db,
        ending_at=ending_at,
    )
    bid = create_random_bid(db, auction.auction_session.minimum_bid_amount)
    crud_auction_session.add_new_bid(db, auction.auction_session, bid)

    time.sleep(5)
    auction = crud_auction.get(db, id=auction.id)
    assert auction.auction_winner_id == bid.usr_id


def test_soft_delete_auction(
        db: Session
) -> None:
    """
    Setting the auction_state to 'canceled' or 'ended'
    """
    pass


def test_get_winner(
        db: Session
) -> None:
    pass


def test_minimum_bid_increases(
        db: Session
) -> None:
    pass


def test_auction_states(
        db: Session
) -> None:
    ending_at = datetime.now() + timedelta(seconds=5)
    bidder = create_random_user(db)
    auction = create_random_auction(
        db=db,
        ending_at=ending_at
    )
    assert auction.auction_session.auction_state == AuctionState.CREATED

    bid = create_random_bid(db, auction.auction_session.minimum_bid_amount)
    crud_auction_session.add_new_bid(db, auction.auction_session, bid)

    assert auction.auction_session.auction_state == AuctionState.ONGOING

    time.sleep(5)
    auction = crud_auction_session.get(
        db=db, id=auction.id)
    assert auction.auction_state == AuctionState.ENDED


def test_get_auction_by_user(
        db: Session
) -> None:
    user = create_random_user(db)
    auction1 = create_random_auction(db, user=user)
    auction2 = create_random_auction(db, user=user)

    auctions_in_db = crud_auction.get_multi_by_owner(
        db=db,
        usr_id=user.id,
    )

    assert auctions_in_db
    assert auctions_in_db[0].id == auction1.id
    assert auctions_in_db[1].id == auction2.id
