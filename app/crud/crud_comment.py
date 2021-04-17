from typing import List
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate
from app.crud.base import CRUDBase


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def create_with_owner_and_product(db: Session, obj_in: CommentCreate, usr_id: int, prod_id: int) -> Comment:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, usr_id=usr_id, prod_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner_and_product(
        self, db: Session, *, usr_id: int, prod_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.usr_id == usr_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


comment = CRUDComment(Comment)
