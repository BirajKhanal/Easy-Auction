from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session

from app.schemas import sellable, product
from app.crud import crud_product, crud_sellable
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=sellable.Sellable)
def buy_sellable(
        sellable_id: int,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    sellable_item = crud_sellable.sellable.get(
        db=db, id=sellable_id)

    update_sellable = sellable.SellableUpdate(**sellable_item)
    update_sellable.sold = True
    update_sellable.buyer = current_user

    if not sellable_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Sellable With That ID Found")
    if sellable_item.sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product Already Bought")

    return crud_sellable.sellable.update(db=db, db_obj=sellable, obj_in=update_sellable)


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
