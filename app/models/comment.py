from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    detail = Column(String)
    title = Column(String)

    usr_id = Column(Integer, ForeignKey('user.id'))
    prod_id = Column(Integer, ForeignKey('product.id'))
