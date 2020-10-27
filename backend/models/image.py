from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database.setup import Base
from .associations import image_tag_table


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    seed = Column(Integer, nullable=False)
    filename = Column(String(51), nullable=False)
    description = Column(Text)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="images")
    tags = relationship("Tag", secondary=image_tag_table, back_populates="images")
