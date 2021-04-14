from typing import List, Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: Optional[str]


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True
