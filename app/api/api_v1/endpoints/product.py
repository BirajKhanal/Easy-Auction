from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas import product
from app.crud import crud_product
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/products/", response_model=product.Product)
def create_product(
        product: product.ProductCreate,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    return crud_product.product.create_with_owner(db=db, obj_in=product, usr_id=current_user.id)


@router.get("/products", response_model=List[product.Product])
def read_products(
        skip: int = 0,
        limit: int = 5,
        db: Session = Depends(get_db)):
    products = crud_product.product.get_multi(
        db, skip=skip, limit=limit)
    return products


@router.get("/products/me", response_model=List[product.Product])
def read_products_by_user(
        skip: int = 0,
        limit: int = 5,
        current_user=Depends(get_current_active_user),
        db: Session = Depends(get_db)):
    products = crud_product.product.get_multi_by_owner(
        db, usr_id=current_user.id, skip=skip, limit=limit)
    return products


@router.get("/products/{product_id}", response_model=product.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return db_product
