from typing import List
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDAuction(CRUDBase[User, UserCreate, UserUpdate]):
    pass


auction = CRUDAuction(User)

