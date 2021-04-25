from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, HttpUrl

# Discount schema


class DiscountBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    discount_percent: Optional[float]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class DiscountCreate(DiscountBase):
    discount_percent: float
    created_at: datetime


class DiscountUpdate(DiscountBase):
    pass


class Discount(DiscountBase):
    id: Optional[int]


    class Config:
        orm_mode = True

