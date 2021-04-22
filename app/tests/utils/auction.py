from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.crud.auction import (
    auction as crud_auction,
)
from app.models.auction import Auction
from app.models.user import User
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
    categories = [cat1.id, cat2.id, cat3.id]
    product_condition = random_product_condition()
    if not bid_cap:
        bid_cap = random_float()
    quantity = random_int()
    starting_bid = random_float()
    if not ending_at:
        ending_at = datetime.now() + timedelta(days=1)
    if not user:
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
