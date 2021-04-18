from typing import List
from sqlalchemy.orm import Session

from app.models.product import Product, ProductType
from app.crud.base import CRUDBase
from app.schemas.product import ProductCreate, ProductUpdate, InventoryCreate


class CRUDProductCondition(CRUDBase[Product, ProductCreate, ProductUpdate]):
    pass


auction = CRUDProductCondition(Product)