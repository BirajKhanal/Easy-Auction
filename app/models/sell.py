from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product
from app.models.user import User


class Discount(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    discount_percent = Column(Float)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)


class Sellable(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))
    discount_id = Column(Integer, ForeignKey('discount.id'))

    product = relationship("Product")
    discount = relationship('Discount')


class ShoppingSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    usr_id = Column(Integer, ForeignKey('user.id'))
    total = Column(Float)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    owner = relationship('User', back_populates='shopping_session')
    cart = relationship('Cart', back_populates='shopping_session')


class CartItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    sellalbe_id = Column(Integer, ForeignKey('sellable.id'))
    session_id = Column(Integer, ForeignKey('shoppingsession.id'))
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    sellables = relationship("Sellable")
    shopping_session = relationship("ShoppingSession", back_populates='cart')
    owner = relationship("User", back_populates='cart')
