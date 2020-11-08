from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base
from .mixins import Timestamp


class Collection(Base, Timestamp):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text)
    is_archived = Column(Boolean, default=False)

    images = relationship("Image", back_populates="collection")
