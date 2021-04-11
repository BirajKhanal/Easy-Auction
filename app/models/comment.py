from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from app.models.product import Product


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    detail = Column(String)
    title = Column(String)

    usr_id = Column(Integer, ForeignKey('user.id'))
    prod_id = Column(Integer, ForeignKey('product.id'))


