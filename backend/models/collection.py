from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Collection(Base, Timestamp):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text)

    images = relationship("CollectionImage", back_populates="collection")
