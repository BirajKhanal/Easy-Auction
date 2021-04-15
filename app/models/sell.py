from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product
from app.models.user import User

cart_sellable = Table(
    'cart_sellable',
    Base.metadata,
    Column('cart_id', Integer, ForeignKey('cart.id')),
    Column('sellable_id', Integer, ForeignKey('sellable.id'))
)


class Sellable(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    discount = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))

    product = relationship("Product")


class Cart(Base):
    id = Column(Integer, primary_key=True, index=True)
    usr_id = Column(Integer, ForeignKey('user.id'),)

    sellables = relationship("Sellable",
                             secondary=cart_sellable)
    owner = relationship("User", back_populates='cart')
