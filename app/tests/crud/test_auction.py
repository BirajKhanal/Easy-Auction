import time
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.auction import AuctionState
from app.crud.auction import (
    auction as crud_auction,
    auction_session as crud_auction_session,
    auctionable as crud_auctionable
)
from app.crud.product import product as crud_product
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
    ending_at = datetime.now() + timedelta(days=1)
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


def test_bid_in_auction(
    db: Session
):
    auction = create_random_auction(db)
    bidder = create_random_user(db)
    bid_amount1 = auction.auction_session.minimum_bid_amount + random_int()
    bid_amount2 = auction.auction_session.minimum_bid_amount + random_int()
    bid_amount3 = auction.auction_session.minimum_bid_amount + random_int()

    bid1 = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid_amount1,
        bidder_id=bidder.id
    )
    bid2 = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid_amount2,
        bidder_id=bidder.id
    )
    bid3 = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid_amount3,
        bidder_id=bidder.id
    )

    bids_in_db = auction.auction_session.bids

    assert bids_in_db
    assert bids_in_db[0].id == bid1.id
    assert bids_in_db[0].usr_id == bidder.id
    assert bids_in_db[1].id == bid2.id
    assert bids_in_db[1].usr_id == bidder.id
    assert bids_in_db[2].id == bid3.id
    assert bids_in_db[2].usr_id == bidder.id

def test_auction_winner_is_set(
        db: Session
) -> None:
    ending_at = datetime.now() + timedelta(seconds=3)
    current_bidder = create_random_user(db)
    bid_amount = random_float()
    current_auction = create_random_auction(
        db,
        ending_at=ending_at,
    )
    crud_auction_session.bid_in_auction(
        db=db,
        id=current_auction.id,
        bid_amount=bid_amount,
        bidder_id=current_bidder.id
    )
    time.sleep(5)
    current_auction = crud_auction.get(db, id=current_auction.id)
    assert current_auction.auction_winner_id == current_bidder.id


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
    current_auction = create_random_auction(
        db=db,
        ending_at=ending_at
    )
    assert current_auction.auction_session.auction_state == AuctionState.CREATED

    bid_amount = current_auction.auction_session.minimum_bid_amount + random_float()
    crud_auction_session.bid_in_auction(
        db=db,
        id=current_auction.id,
        bid_amount=bid_amount,
        bidder_id=bidder.id
    )
    assert current_auction.auction_session.auction_state == AuctionState.ONGOING

    time.sleep(5)
    current_auction_session = crud_auction_session.get(db=db, id=current_auction.id)
    assert current_auction_session.auction_state == AuctionState.ENDED


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

