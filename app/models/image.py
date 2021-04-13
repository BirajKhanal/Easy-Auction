from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    img_url = Column(String, nullable=False)

    usr_id = Column(Integer, ForeignKey('user.id'))
    prod_id = Column(Integer, ForeignKey('product.id'))

    owner = relationship('User', back_populates='images')
    product = relationship('Product', back_populates='images')
