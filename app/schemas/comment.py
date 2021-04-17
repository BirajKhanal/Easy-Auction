from typing import List, Optional

from pydantic import BaseModel
from app.schemas.user import User
from app.schemas.product import Product


class CommentBase(BaseModel):
    detail: Optional[str]
    title: Optional[str]
    usr_id: Optional[int]
    prod_id: Optional[int]


class CommentCreate(CommentBase):
    title: str
    detail: str
    usr_id: int
    prod_id: int


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: Optional[int]

    class Config:
        orm_mode = True
