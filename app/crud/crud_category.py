from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.crud.base import CRUDBase


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_with_name(self, db: Session, name: str) -> Category:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_multi_categories(self, db: Session, categories: List[str]) -> List[Category]:
        cat_list: List[Category] = []
        for item in categories:
            # TODO: if frontend sends category_id change this and schema too
            cat_item = self.get_with_name(db=db, name=item)
            if cat_item is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Category {item} Not Available")
            cat_list.append(cat_item)
        return cat_list


category = CRUDCategory(Category)
