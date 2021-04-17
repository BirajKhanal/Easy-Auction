from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    img_url = Column(String, nullable=False)
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    usr_id = Column(Integer, ForeignKey('user.id'))

    owner = relationship('User')
