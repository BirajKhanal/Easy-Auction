from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product
from app.models.user import User


# stores available discounts
class Discount(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    discount_percent = Column(Float)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)


# stores the info for product that can be sold
class Sellable(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))
    discount_id = Column(Integer, ForeignKey('discount.id'))

    product = relationship("Product", back_populates='sellable')
    discount = relationship('Discount')


class ShoppingSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    usr_id = Column(Integer, ForeignKey('user.id'))
    total = Column(Float)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    owner = relationship('User', back_populates='shopping_session')
    cart = relationship('CartItem', back_populates='shopping_session')


class CartItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    sellalbe_id = Column(Integer, ForeignKey('sellable.id'))
    session_id = Column(Integer, ForeignKey('shoppingsession.id'))
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    sellables = relationship("Sellable")
    shopping_session = relationship("ShoppingSession", back_populates='cart')



class CartLog(Base):
    id = Column(Integer, primary_key=True, index=True)
    cartitem_id = Column(Integer, ForeignKey('cartitem.id'))
    quantity = Column(Integer)
    created_at = Column(DateTime)

    cartitem = relationship("CartItem")
