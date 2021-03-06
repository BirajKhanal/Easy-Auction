import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.user import User
from app.models.comment import Comment


class ProductCondition(str, enum.Enum):
    BRAND_NEW = 'brandnew'
    BEST = 'best'
    GOOD = 'good'
    POOR = 'poor'


product_category = Table('product_category', Base.metadata, Column('product_id', Integer, ForeignKey('product.id')),
                         Column('category_id', Integer, ForeignKey('category.id')))

product_comment = Table('product_comment', Base.metadata, Column('product_id', Integer, ForeignKey('product.id')),
                        Column('comment_id', Integer, ForeignKey('comment.id')))

product_image = Table('product_image', Base.metadata, Column('product_id', Integer, ForeignKey('product.id')),
                      Column('image_id', Integer, ForeignKey('image.id')))


# Inventory stores the current inventory of a specific product
# if quantity == 0  then the product currently no available
class Inventory(Base):
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1)
    restocked_at = Column(DateTime)

    product = relationship('Product', back_populates='inventory')


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    product_condition = Column(Enum(ProductCondition))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    usr_id = Column(Integer, ForeignKey('user.id'))

    auctionable = relationship("Auctionable", back_populates='product')
    sellable = relationship("Sellable", back_populates='product')
    owner = relationship("User", back_populates='products')
    inventory = relationship(
        'Inventory', back_populates='product')
    comments = relationship("Comment", secondary=product_comment)
    images = relationship("Image", secondary=product_image)
    categories = relationship(
        "Category", secondary=product_category, back_populates="products")


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    products = relationship(
        "Product", secondary=product_category, back_populates="categories")
