from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    product_condition = Column(String)
    reserv = Column(Integer)

    auction = relationship("Auction", back_populates="items")


class Auction(Base):
    __tablename__ = "auction"

    id = Column(Integer, primary_key=True, index=True)
    # starting_date = Column(Integer)
    # ending_date = Column(Integer)
    selling_price = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))

    items = relationship("Product", back_populates="auction")
