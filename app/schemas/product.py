from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    description: Optional[str] = None
    product_condition: str


class ProductCreate(ProductBase):
    name: str
    category: str
    reserv: int


class Product(ProductBase):
    id: int
    # auction: List[Auction] = []

    class Config:
        orm_mode = True
