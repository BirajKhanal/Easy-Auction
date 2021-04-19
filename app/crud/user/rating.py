from typing import List
from sqlalchemy.orm import Session

from app.models.user import Rating
from app.schemas.user import RatingCreate, RatingUpdate
from app.crud.base import CRUDBase


class CRUDRating(CRUDBase[Rating, RatingCreate, RatingUpdate]):
    pass


rating = CRUDRating(Rating)
