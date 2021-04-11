from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.auction import Auction


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    product_condition = Column(String)
    reserv = Column(Integer)

    auction = relationship("Auction", back_populates="items")
