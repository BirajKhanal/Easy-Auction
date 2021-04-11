from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    product_condition = Column(String)
    img = Column(String)

    usr_id = Column(Integer, ForeignKey('user.id'))


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Product_Category(Base):
    id = Column(Integer, primary_key=True, index=True)

    cat_id = Column(Integer, ForeignKey('category.id'))
    prod_id = Column(Integer, ForeignKey('product.id'))
