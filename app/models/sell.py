from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product
from app.models.user import User


class Sellable(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    discount = Column(Float)
    quantity = Column(Integer)

    prod_id = Column(Integer, ForeignKey('product.id'))

class Cart(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)

    prod_sell = Column(Integer, ForeignKey('product.id'))

