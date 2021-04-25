from typing import List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import ProductCondition
from app.models.user import User
from app.models.auction import AuctionState, AuctionSession, BID_INCREASE_AMOUNT
from app.api.dependencies import get_db, get_current_active_user
from app.schemas.product import ProductCreate
from app.schemas.auction import Auction, Bid, BidCreate, AuctionCreate, AuctionableCreate, AuctionSessionCreate
from app.crud.product.category import category as crud_category
from app.crud.auction import auction as crud_auction
from app.crud.auction.auction_session import auction_session as crud_auction_session, is_auction_ended
from app.crud.auction.auctionable import auctionable as crud_auctionable
from app.crud.auction import bid as crud_bid

router = APIRouter()


@router.get('/{id}', response_model=Auction)
def get_auction(
    id: int,
    db: Session = Depends(get_db)
):
    auction = crud_auction.get_complete(
        db=db,
        id=id
    )
    if not auction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="auction of specified ID dose not exists"
        )
    return auction


@router.put('/{id}')
def update_auction(
    name: str = Body(None),
    categories: List[int] = Body(None),
    description: str = Body(None),
    product_condition: ProductCondition = Body(None),
    quantity: int = Body(None),
    bid_cap: float = Body(None),
    starting_bid: float = Body(None),
    ending_at: str = Body(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    pass


@router.post('/{id}/bid', response_model=Bid)
def bid_in_auction(
    id: int,
    bid_amount: float = Body(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    auction = crud_auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="auction with that ID not found"
        )

    # check if auction ended or canceled
    auction_session: AuctionSession = auction.auction_session
    state_list = [AuctionState.ENDED, AuctionState.CANCELED]

    if is_auction_ended(auction_session):
        if auction_session.auction_state not in state_list:
            auction_session = crud_auction_session.update_auction_state(
                db, auction_session, AuctionState.ENDED)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"the auction with that ID has already been {auction_session.auction_state}")

    if bid_amount < auction_session.minimum_bid_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="bid amount must be greater than minimum bid amount"
        )

    bid_obj = BidCreate(bid_amount=bid_amount, usr_id=current_user.id)
    bid_db = crud_bid.create(db, obj_in=bid_obj)

    return crud_auction_session.add_new_bid(db, db_obj=auction_session, bid_db=bid_db)


@router.get('/{id}/bid', response_model=List[Bid])
def get_auction_bids(
    id: int,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    auction = crud_auction.get(db=db, id=id)
    if not auction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="auction with that id not found"
        )
    # return crud_auction_session.get_bids(db=db,
    # id=auction.auction_session_id, skip=skip, limit=limit)
    return crud_bid.get_multi_by_auction_id(
        db, auction_id=auction.id, skip=skip, limit=limit)


@router.post('/', response_model=Auction)
def create_auction(
    name: str = Body(...),
    categories: List[int] = Body(None),
    description: str = Body(None),
    product_condition: ProductCondition = Body(None),
    quantity: int = Body(None),
    bid_cap: float = Body(...),
    starting_bid: float = Body(...),
    ending_at: datetime = Body(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if starting_bid > bid_cap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="starting bid should be greater than bid cap"
        )

    if ending_at <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ending date should be greater than today's date"
        )

    categories = crud_category.get_multi_by_ids(
        db=db, category_ids=categories)

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
        usr_id=current_user.id,
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
        owner_id=current_user.id
    )

    auction_db = crud_auction.create(db, obj_in=auction_obj)

    return auction_db


@router.get('/', response_model=List[Auction])
def get_auctions(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    return crud_auction.get_multi(db=db, skip=skip, limit=limit)

# TODO: route for canceling auction
# TODO: route for getting auctions set by specific user
# TODO: route for getting all  bids by specific user in specific auction
# TODO: route for getting all bids by specific user
