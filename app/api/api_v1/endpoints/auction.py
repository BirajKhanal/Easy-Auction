from typing import List
from datetime import timedelta, datetime
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import ProductCondition
from app.models.user import User
from app.api.dependencies import get_db, get_current_active_user
from app.schemas.auction import Auction, Bid
from app.crud.auction import auction as crud_auction
from app.crud.auction import auction_session as crud_auction_session
from app.crud.auction import bid as crud_bid

router = APIRouter()


@router.get('/{id}', response_model=Auction)
def get_auction(
    id: int,
    db: Session = Depends(get_db)
):
    auction = crud_auction.get(
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
            detail="specified auction not found"
        )
    # TODO: raise exception if auction_state in ['ENDED', 'CANCELED']
    return crud_auction_session.bid_in_auction(
        db=db,
        id=auction.auction_session_id,
        bid_amount=bid_amount,
        bidder_id=current_user.id
    )


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
    return crud_bid.get_multi_by_auction(db=db, auction_session_id=auction.auction_session_id, skip=skip, limit=limit)


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
    # TODO: validation for ending_at should be greater than today's date
    # TODO: validation for starting_bid should be less than bid_cap
    auction_db = crud_auction.create_with_owner(
        db=db,
        name=name,
        description=description,
        categories=categories,
        product_condition=product_condition,
        quantity=quantity,
        bid_cap=bid_cap,
        starting_bid=starting_bid,
        ending_at=ending_at,
        usr_id=current_user.id
    )
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
