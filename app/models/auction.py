from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Auction(Base):
    id = Column(Integer, primary_key=True, index=True)
    # starting_date = Column(Integer)
    # ending_date = Column(Integer)
    selling_price = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.id"))

    items = relationship("Product", back_populates="auction")
