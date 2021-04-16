from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    detail = relationship('UserDetail', back_populates='user')
    comments = relationship('Comment', back_populates='owner')
    products = relationship('Product', back_populates='owner')
    shopping_session = relationship('ShoppingSession', back_populates='owner')
    rating = relationship('Rating', back_populates='user')


class UserDetail(Base):
    id = Column(Integer, primary_key=True, index=True)
    usr_id = Column(Integer, ForeignKey('user.id'))
    profile_pic_id = Column(Integer, ForeignKey('image.id'))
    description = Column(String)

    user = relationship('User', back_populates='detail')
    profile_pic = relationship('Image')


class Rating(Base):
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=True)
    usr_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='rating')
