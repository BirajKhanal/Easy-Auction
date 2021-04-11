from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rating = relationship("Rating")
    # is_active = Column(Boolean(), default=True)


class Rating(Base):
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=True)

    usr_id = Column(Integer, ForeignKey('user.id'))
