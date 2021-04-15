from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import sellable, product, cart
from app.crud import crud_product, crud_sellable, crud_cart
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=sellable.Sellable)
def create_sellable(
        product_in: product.ProductCreate,
        sellable_in: sellable.SellableCreate,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    new_product = crud_product.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=current_user.id)
    return crud_sellable.sellable.create_with_product(
        db=db, obj_in=sellable_in, product=new_product)


@router.get("/", response_model=List[sellable.Sellable])
def get_sellable(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    sellable = crud_sellable.sellable.get_multi(
        db=db, skip=skip, limit=limit
    )
    return sellable


@router.post("/make", response_model=sellable.Sellable)
def make_product_sellable(
    sellable_in: sellable.SellableCreate,
    prod_id: int = Body(...),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    product = crud_product.product.get(db=db, id=prod_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Product With That ID Exists")
    return crud_sellable.sellable.create_with_product(
        db=db, obj_in=sellable_in, product=product)


@router.get('/cart/me', response_model=cart.Cart)
def get_user_cart(
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    return crud_cart.cart.get_by_user(db=db, user=current_user)


@router.post('/add_to_cart', response_model=cart.Cart)
def add_to_cart(
    sellable_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud_cart.cart.add_to_cart_by_user(db=db, sellable_id=sellable_id, user=current_user)


@router.get("/user/{usr_id}", response_model=List[sellable.Sellable])
def get_sellable_by_user(
    usr_id: int,
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    sellable = crud_sellable.sellable.get_multi_by_owner(
        db=db, usr_id=usr_id, skip=skip, limit=limit
    )
    return sellable
