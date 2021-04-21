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
from app.models.auction import Auction
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_int, random_float
from app.tests.utils.product import create_random_category, random_product_condition


def create_random_auction(db: Session) -> Auction:
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

    return crud_auction.create_with_owner(
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
