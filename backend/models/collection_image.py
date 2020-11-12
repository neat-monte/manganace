from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class CollectionImage(Base):
    __tablename__ = "collection_images"

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    image_id = Column(Integer, ForeignKey('images.id'))

    collection = relationship("Collection", back_populates="images")
    image = relationship("Image", back_populates="collection_images")
    tags = relationship("Tag", secondary='collection_image_tag', back_populates="images")
