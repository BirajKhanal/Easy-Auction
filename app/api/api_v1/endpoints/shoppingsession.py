from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import sellable
from app.crud.sell import shopping_session as crud_shopping_session
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=sellable.ShoppingSession)
def create_shopping_session():
    return "works"


@router.get("/", response_model=List[sellable.ShoppingSession])
def get_shopping_session():
    return "works"
