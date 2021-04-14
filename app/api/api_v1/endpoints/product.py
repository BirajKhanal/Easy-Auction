from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schemas import product, category
from app.crud import crud_product, crud_category
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=product.Product)
def create_product(
        product_in: product.ProductCreate,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    return crud_product.product.create_with_owner(db=db, obj_in=product_in, usr_id=current_user.id)


@router.get("/", response_model=List[product.Product])
def read_products(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    products = crud_product.product.get_multi(
        db=db, skip=skip, limit=limit)
    return products


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
