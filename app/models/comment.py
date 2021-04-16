from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    detail = Column(String)
    title = Column(String)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    usr_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('User', back_populates='comments')
