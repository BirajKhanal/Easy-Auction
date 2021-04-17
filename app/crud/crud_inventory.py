from sqlalchemy.orm import Session
from datetime import datetime
from app.models.product import Inventory
from app.schemas.product import InventoryCreate, InventoryUpdate
from app.crud.base import CRUDBase


class CRUDInventory(CRUDBase[Inventory, InventoryCreate, InventoryUpdate]):
    def create(self, db: Session, obj_in: InventoryCreate, restocked_at: datetime) -> Inventory:
        inventory = super().create(db=db, obj_in=obj_in)
        inventory.restocked_at = restocked_at
        db.add(inventory)
        db.commit()
        db.refresh(inventory)
        return inventory


inventory = CRUDInventory(Inventory)
