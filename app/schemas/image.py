from typing import List, Optional

from pydantic import BaseModel, HttpUrl
from app.schemas.user import User
from app.schemas.sellable import Sellable


class ImageBase(BaseModel):
    description: Optional[str]
    img_url: Optional[HttpUrl]
    usr_id: Optional[int]
    prod_id: Optional[int]


class ImageCreate(ImageBase):
    img_url: Optional[HttpUrl]
    usr_id: Optional[int]
    prod_id: Optional[int]


class ImageUpdate(ImageBase):
    pass


class Image(ImageBase):
    id: Optional[int]

    class Config:
        orm_mode = True
