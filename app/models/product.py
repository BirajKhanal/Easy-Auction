import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User
from app.models.comment import Comment


class ProductType(str, enum.Enum):
    AUCTIONABLE = 'AUCTIONABLE'
    SELLABLE = 'SELLABLE'
    BOTH = 'BOTH'


product_category = Table('product_category', Base.metadata, Column('product_id', Integer, ForeignKey('product.id')),
                         Column('category_id', Integer, ForeignKey('category.id')))


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    product_condition = Column(String)
    sold = Column(Boolean, default=False)
    product_type = Column(Enum(ProductType), nullable=False, index=True)

    usr_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship("User", back_populates='products')
    comments = relationship("Comment", back_populates="product")
    images = relationship("Image", back_populates="product")
    categories = relationship(
        "Category", secondary=product_category, back_populates="products")


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship(
        "Product", secondary=product_category, back_populates="categories")
