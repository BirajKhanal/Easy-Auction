from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_with_name(self, db: Session, name: str) -> Category:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_multi_by_ids(self, db: Session, category_ids: List[int]) -> List[Category]:
        cat_list: List[Category] = []
        for category_id in category_ids:
            cat_item = self.get(db=db, id=category_id)
            cat_list.append(cat_item)
        return cat_list


category = CRUDCategory(Category)
