from typing import List
from sqlalchemy.orm import Session

from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from app.crud.base import CRUDBase


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    pass


image = CRUDImage(Image)
