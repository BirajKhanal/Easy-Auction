import time
from typing import Dict
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.auction import AuctionState
from app.crud.auction.auction import auction as crud_auction
from app.crud.auction.auction_session import auction_session as crud_auction_session
from app.crud.auction.auctionable import auctionable as crud_auctionable
from app.core.config import settings
from app.tests.utils.utils import random_lower_string, random_float, random_int
from app.tests.utils.product import random_product_condition, create_random_category
from app.tests.utils.auction import create_random_auction
from app.tests.utils.user import create_random_user


def test_create_auction(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str]
) -> None:
    name = random_lower_string()
    cat1 = create_random_category(db)
    cat2 = create_random_category(db)
    cat3 = create_random_category(db)
    description = random_lower_string()
    product_condition = random_product_condition().value
    quantity = random_int()
    ending_at = datetime.now() + timedelta(days=5)
    bid_cap = random_float()
    starting_bid = bid_cap - (bid_cap/3)
    auction_data = {
        "name": name,
        "categories": [
            cat1.id,
            cat2.id,
            cat3.id
        ],
        "description": description,
        "product_condition": product_condition,
        "quantity": quantity,
        "bid_cap": bid_cap,
        "starting_bid": starting_bid,
        "ending_at": ending_at.isoformat()
    }
    r = client.post(f"{settings.API_V1_STR}/auction/",
                    headers=normal_user_token_headers,
                    json=auction_data
                    )
    assert 200 <= r.status_code < 300

    created_auction = r.json()

    auction_in_db = crud_auction.get(db=db, id=created_auction.get("id"))

    assert auction_in_db
    assert auction_in_db.name == name
    assert auction_in_db.auction_session
    assert auction_in_db.auction_session.minimum_bid_amount == starting_bid
    assert auction_in_db.auction_session.auction_state == AuctionState.CREATED
    assert auction_in_db.auction_session.ending_at == ending_at

    auctionable_in_db = crud_auctionable.get(
        db, id=auction_in_db.auctionable_id)
    assert auctionable_in_db
    assert auctionable_in_db.bid_cap == bid_cap
    assert auctionable_in_db.starting_bid == starting_bid

    assert auctionable_in_db.product.name == name
    assert auctionable_in_db.product.description == description
    assert auctionable_in_db.product.product_condition == product_condition

    assert auctionable_in_db.product.inventory.quantity == quantity


def test_create_auction_with_invalid_ending_at(
        client: TestClient,
        db: Session,
        normal_user_token_headers: Dict[str, str]
) -> None:
    ending_at = datetime.now() - timedelta(days=5)
    bid_cap = random_float()
    starting_bid = bid_cap - (bid_cap/3)
    auction_data = {
        "name": random_lower_string(),
        "categories": [
            create_random_category(db).id,
            create_random_category(db).id,
            create_random_category(db).id
        ],
        "description": random_lower_string(),
        "product_condition": random_product_condition().value,
        "quantity": random_int(),
        "bid_cap": bid_cap,
        "starting_bid": starting_bid,
        "ending_at": ending_at.isoformat()
    }
    r = client.post(f"{settings.API_V1_STR}/auction/",
                    headers=normal_user_token_headers,
                    json=auction_data
                    )
    print(r.json())
    assert r.status_code == 400


def test_bid_in_auction(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str]
):
    auction = create_random_auction(db)
    bid_amount = auction.auction_session.minimum_bid_amount + random_float()
    r = client.post(f"{settings.API_V1_STR}/auction/{auction.id}/bid",
                    headers=normal_user_token_headers,
                    json=bid_amount
                    )
    assert 200 <= r.status_code < 300
    created_bid = r.json()
    bids_in_db = auction.auction_session.bids

    assert created_bid["bid_amount"] == bid_amount
    assert bids_in_db
    assert bids_in_db[0].bid_amount == bid_amount


def test_bid_in_auction_with_invalid_starting_bid(
        client: TestClient,
        db: Session,
        normal_user_token_headers: Dict[str, str]
) -> None:
    auction = create_random_auction(db)
    bid_amount = auction.auction_session.minimum_bid_amount - 10
    r = client.post(f"{settings.API_V1_STR}/auction/{auction.id}/bid",
                    headers=normal_user_token_headers,
                    json=bid_amount
                    )
    assert r.status_code == 400


def test_bid_in_already_finished_auction(
        client: TestClient,
        db: Session,
        normal_user_token_headers: Dict[str, str]

) -> None:
    ending_at = datetime.now()
    auction = create_random_auction(db, ending_at=ending_at)
    bid_amount = auction.auction_session.minimum_bid_amount + random_float()
    time.sleep(3)
    r = client.post(f"{settings.API_V1_STR}/auction/{auction.id}/bid",
                    headers=normal_user_token_headers,
                    json=bid_amount
                    )
    print(r.json())
    assert r.status_code == 400


def test_get_specific_user_auction(
        client: TestClient,
        db: Session
) -> None:
    pass


def test_get_auction_bid(
    client: TestClient,
    db: Session,
):
    auction = create_random_auction(db)
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    user3 = create_random_user(db)
    bid1 = random_float()
    bid2 = random_float()
    bid3 = random_float()

    bid1_in_db = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid1,
        bidder_id=user1.id
    )
    bid2_in_db = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid2,
        bidder_id=user2.id
    )
    bid3_in_db = crud_auction_session.bid_in_auction(
        db=db,
        id=auction.id,
        bid_amount=bid3,
        bidder_id=user3.id
    )

    r = client.get(f"{settings.API_V1_STR}/auction/{auction.id}/bid")
    assert 200 <= r.status_code < 300
    bids_in_response = r.json()
    print(bids_in_response)

    assert bids_in_response[0]["id"] == bid1_in_db.id
    assert bids_in_response[1]["id"] == bid2_in_db.id
    assert bids_in_response[2]["id"] == bid3_in_db.id


def test_cancel_bid(
        client: TestClient,
        db: Session
) -> None:
    pass
