from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import user as crud_user
from app.api import dependencies
from app.core.config import settings

router = APIRouter()


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.user.User = Depends(
        dependencies.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud_user.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(dependencies.get_db),
    current_user: models.user.User = Depends(
        dependencies.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud_user.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=password, email=email, full_name=full_name)
    user = crud_user.user.create(db, obj_in=user_in)
    return user


@router.get("/{usr_id}", response_model=schemas.User)
def get_user(
    usr_id: int,
    db: Session = Depends(dependencies.get_db)
):
    user = crud_user.user.get(db=db, id=usr_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return user


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(
        dependencies.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = crud_user.user.get_multi(db, skip=skip, limit=limit)
    return users
