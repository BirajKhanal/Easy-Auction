from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product


class Auctionable(Base):
    id = Column(Integer, primary_key=True, index=True)
    # starting_date = Column(Integer)
    # ending_date = Column(Integer)
    bid_cap = Column(Float)
    starting_bid = Column(Float)
    prod_id = Column(Integer, ForeignKey('product.id'))

    product = relationship("Product")


class Auction(Base):
    id = Column(Integer, primary_key=True, index=True)
    duration = Column(Float)
    start_timestamp = Column(DateTime)
    current_bid = Column(Float)
    prod_auc_id = Column(Integer, ForeignKey('auctionable.id'))

    auctionable = relationship("Auctionable")
