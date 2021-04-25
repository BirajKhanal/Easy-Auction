from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import cart
from app.crud.sell import cart_item
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=cart.Cart)
def create_cart_item():
    return "works"


@router.get("/", response_model=List[cart.Cart])
def get_cart_item():
    return "works"
