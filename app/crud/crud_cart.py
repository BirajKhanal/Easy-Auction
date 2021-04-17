# from typing import List
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status

# from app.models.sell import Cart
# from app.models.user import User
# from app.schemas.cart import CartCreate, CartUpdate
# from app.crud.base import CRUDBase
# from app.crud.crud_sellable import sellable


# class CRUDCart(CRUDBase[Cart, CartCreate, CartUpdate]):
#     def get_by_user(self, db: Session, user: User) -> Cart:
#         return db.query(self.model).filter(self.model.usr_id == user.id).first()

#     def add_to_cart_by_user(self, db: Session, sellable_id: int, user: User) -> Cart:
#         sellable_db = sellable.get(db=db, id=sellable_id)
#         if (not sellable_db or (sellable_db.product.sold)):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="Product Is Not Available")
#         cart = self.get_by_user(db=db, user=user)
#         if not cart:
#             cart = self.model(sellables=[sellable_db], owner=user)
#         else:
#             sellables = cart.sellables
#             sellables.append(sellable_db)
#             cart.sellables = sellables
#         db.add(cart)
#         db.commit()
#         db.refresh(cart)
#         return cart


# cart = CRUDCart(Cart)
