from typing import List, Union
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import product, category, auction, sellable
from app import crud
from app.api.dependencies import get_db, get_current_active_user
from app.models.product import ProductType

router = APIRouter()


@router.post("/", response_model=product.ProductResponse, response_model_exclude_unset=True)
def create_product(
        product_in: product.ProductCreateRequest,
        product_type: ProductType,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):

    product_in: dict = product_in.dict()
    product_obj = product.ProductCreate(**product_in)
    product_db = crud.product.create_with_owner(
        db=db,
        obj_in=product_obj,
        usr_id=current_user.id,
        product_type=product_type,
        quantity=product_in.get('quantity', 1)
    )
    prod_obj = jsonable_encoder(product_db)
    if product_type in [ProductType.SELLABLE, ProductType.BOTH]:
        sellable_obj = sellable.SellableCreate(**product_in)
        sellable_product = crud.sellable.create_with_product(
            db=db, obj_in=sellable_obj, product_id=product_db.id
        )
        prod_obj = {**prod_obj, **jsonable_encoder(sellable_product)}

    if product_type in [ProductType.AUCTIONABLE, ProductType.BOTH]:
        auction_obj = auction.AuctionableCreate(**product_in)
        auctionable_product = crud.auctionable.create_with_product(
            db=db, obj_in=auction_obj, product_id=product_db.id
        )
        prod_obj = {**prod_obj, **jsonable_encoder(auctionable_product)}

    return product.ProductResponse(**prod_obj, categories=product_db.categories, inventory=product_db.inventory)


@router.get("/", response_model=List[product.Product])
def read_products(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    products = crud.product.get_multi(
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
