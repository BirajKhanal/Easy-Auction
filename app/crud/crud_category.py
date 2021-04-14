from typing import List
from sqlalchemy.orm import Session

from app.models.product import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_with_name(self, db: Session, name: str):
        return db.query(self.model).filter(self.model.name == name).first()

    def get_multi_categories(self, db: Session, categories: List[str]) -> List[Category]:
        cat_list: List[Category] = []
        for item in categories:
            cat_list.append(self.get_with_name(db=db, name=item))
        return cat_list


category = CRUDCategory(Category)
