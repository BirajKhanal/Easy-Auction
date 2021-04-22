from typing import List
from sqlalchemy.orm import Session

from app.models.product import Product, ProductType
from app.crud.base import CRUDBase
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate


class CRUDDiscount(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


auction = CRUDDiscount(Product)
