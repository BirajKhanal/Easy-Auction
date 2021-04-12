from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas import product
from app.crud import crud_product
from app.api.dependencies import get_db

router = APIRouter()


@router.post("/products/", response_model=product.Product)
def create_product(product: product.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)


@router.get("/products", response_model=List[product.Product])
def read_products(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/products/{product_id}", response_model=product.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return db_product
