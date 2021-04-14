from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session

from app.schemas import auction, product, category
from app.crud import crud_product, crud_auctionable
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=auction.Auctionable)
def create_auctionable(
        product_in: product.ProductCreate,
        auctionable_in: auction.AuctionableCreate,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    new_product = crud_product.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=current_user.id)
    return crud_auctionable.auctionable.create_with_product(
        db=db, obj_in=auctionable_in, product=new_product)


@router.post("/make", response_model=auction.Auctionable)
def make_product_auctionable(
    auctionable_in: auction.AuctionableCreate,
    prod_id: int = Body(...),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = crud_product.product.get(db=db, id=prod_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Product With That ID Exists")
    return crud_auctionable.auctionable.create_with_product(
        db=db, obj_in=auctionable_in, product=product)


@router.get("/", response_model=List[auction.Auctionable])
def get_auctionable(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    auctionable = crud_auctionable.auctionable.get_multi(
        db=db, skip=skip, limit=limit
    )
    return auctionable


@router.get("/user/{usr_id}", response_model=List[auction.Auctionable])
def get_auctionable_by_user(
    usr_id: int,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    auctionable = crud_auctionable.auctionable.get_multi_by_owner(
        db=db, usr_id=usr_id, skip=skip, limit=limit
    )
    return auctionable
