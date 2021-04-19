from typing import List
from sqlalchemy.orm import Session

from app.models.user import UserDetail
from app.schemas.user import UserDetailCreate, UserDetailUpdate
from app.crud.base import CRUDBase


class CRUDUserDetail(CRUDBase[UserDetail, UserDetailCreate, UserDetailUpdate]):
    pass


user_detail = CRUDUserDetail(UserDetail)
