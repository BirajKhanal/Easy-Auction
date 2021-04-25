from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.models.product import ProductCondition
from app.schemas.sellable import Sellable
from app.crud.sell import sellable as crud_sellable
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.get("/{id}", response_model=Sellable)
def get_sellable(id: int, db: Session = Depends(get_db)):
    sellable = crud_sellable.get(db=db, id=id)

    if not sellable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="sellable of specified ID does not exists"
        )

    return sellable


@router.post("/", response_model=Sellable)
def create_sellable(
    name: str = Body(...),
    description: str = Body(None),
    categories: List[int] = Body(None),
    product_condition: ProductCondition = Body(None),
    quantity: int = Body(None),
    price: float = Body(...),
    usr_id: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    
    sellable_db = crud_sellable.create_sellable(
        db=db,
        name=name,
        description=description,
        categories=categories,
        product_condition=product_condition,
        quantity=quantity,
        price=price,
        usr_id=usr_id.id,
    )

    return sellable_db
