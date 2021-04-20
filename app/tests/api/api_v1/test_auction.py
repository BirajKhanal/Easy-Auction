from typing import Dict
from datetime import datetime
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.auction.auction import auction as crud_auction
from app.crud.auction.auction_session import auction_session as crud_auction_session
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string, random_float, random_int
from app.tests.utils.product import random_product_condition, create_random_category
from app.tests.utils.auction import create_random_auction


def test_create_auction(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str]
) -> None:
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
        "bid_cap": random_float(),
        "starting_bid": random_float(),
        "ending_at": datetime.now().isoformat()
    }
    r = client.post(f"{settings.API_V1_STR}/auction/",
                    headers=normal_user_token_headers,
                    json=auction_data
                    )
    created_auction = r.json()

    auction_in_db = crud_auction.get(db=db, id=created_auction.get("id"))

    assert 200 <= r.status_code < 300
    assert auction_in_db


def test_bid_in_auction(
    client: TestClient,
    db: Session,
    normal_user_token_headers: Dict[str, str]
):
    auction = create_random_auction(db)
    bid_amount = random_float()
    bid_data = {
        "bid_amount": bid_amount
    }
    r = client.post(f"{settings.API_V1_STR}/auction/{auction.id}/bid",
                    headers=normal_user_token_headers,
                    json=bid_amount
                    )
    print(f"{settings.API_V1_STR}/auction/{auction.id}/bid")
    assert 200 <= r.status_code < 300
    created_bid = r.json()
    print()
    bids_in_db = crud_auction_session.get_bids(
        db=db, id=auction.auction_session_id)

    assert bids_in_db
    assert bids_in_db[0].bid_amount == bid_amount


def test_get_auction_bid(
    db: Session
):
    pass
