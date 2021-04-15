from typing import List, Union
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import product, category, auction, sellable
from app.crud import crud_product, crud_category, crud_sellable, crud_auctionable
from app.api.dependencies import get_db, get_current_active_user
from app.models.product import ProductType

router = APIRouter()


@router.post("/", response_model=product.Product)
def create_product(
        product_in: product.ProductCreate,
        auctionable_in: auction.AuctionableCreate,
        sellable_in: sellable.SellableCreate,
        product_type: ProductType,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    product_db = crud_product.product.create_with_owner(
        db=db, obj_in=product_in, usr_id=current_user.id, product_type=product_type)
    if product_type == ProductType.SELLABLE:
        sellable_product = crud_sellable.sellable.create_with_product(
            db=db, obj_in=sellable_in, product=product_db
        )

    elif product_type == ProductType.AUCTIONABLE:
        auctionable_product = crud_auctionable.auctionable.create_with_product(
            db=db, obj_in=auctionable_in, product=product_db
        )

    else:
        sellable_product = crud_sellable.sellable.create_with_product(
            db=db, obj_in=sellable_in, product=product_db
        )
        auctionable_product = crud_auctionable.auctionable.create_with_product(
            db=db, obj_in=auctionable_in, product=product_db
        )

    return product_db


@router.get("/", response_model=List[product.Product])
def read_products(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    products = crud_product.product.get_multi(
        db=db, skip=skip, limit=limit)
    return products


@router.post("/buy", response_model=product.Product)
def buy_sellable_product(
        product_id: int,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    product_db = crud_product.product.get(
        db=db, id=product_id)

    if not product_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Prodcut With That ID Found")
    if product_db.sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product Already Bought")
    if (product_db.product_type not in [ProductType.SELLABLE, ProductType.BOTH]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Product Can't Be Bought"
        )
    return crud_product.product.buy_product(db=db, db_obj=product_db, buyer=current_user)


@router.get("/user/{usr_id}", response_model=List[product.Product])
def read_products_by_user(
        usr_id: int,
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    products = crud_product.product.get_multi_by_owner(
        db, usr_id=usr_id, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=product.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    return db_product
