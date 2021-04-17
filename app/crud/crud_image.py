from typing import List
from sqlalchemy.orm import Session

from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from app.crud.base import CRUDBase


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create_with_owner_and_product(db: Session, obj_in: ImageCreate, usr_id: int, prod_id: int) -> Image:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, usr_id=usr_id, prod_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner_and_product(
        self, db: Session, *, usr_id: int, prod_id: int, skip: int = 0, limit: int = 100
    ) -> List[Image]:
        return (
            db.query(self.model)
            .filter(Image.usr_id == usr_id)
            .filter(Image.prod_id == prod_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


image = CRUDImage(Image)
