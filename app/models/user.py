from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    images = relationship("Image")
    rating = relationship("Rating")
    comments = relationship('Comment', back_populates='owner')
    products = relationship('Product', back_populates='owner')
    cart = relationship('Cart', back_populates='owner')


class Rating(Base):
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=True)

    usr_id = Column(Integer, ForeignKey('user.id'))
