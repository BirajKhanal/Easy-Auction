from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas import sellable
from app.crud.sell import sellable as crud_sellable
from app.api.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=sellable.Sellable)
def create_sellable():
    return "works"


@router.get("/", response_model=List[sellable.Sellable])
def get_sellable():
    return "works"
