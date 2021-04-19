from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.schemas import category
from app.crud import product as crud_product
from app.api.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=category.Category)
def create_category(
        category_in: category.CategoryCreate,
        db: Session = Depends(get_db)):
    get_category = crud_product.category.get_with_name(db, category_in.name)
    if get_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category Already Exists")
    return crud_category.category.create(db, obj_in=category_in)


@router.get("/", response_model=List[category.Category])
def get_category(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    category_list = crud_category.category.get_multi(
        db=db, skip=skip, limit=limit)
    if not category_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Category Exists")
    return category_list
