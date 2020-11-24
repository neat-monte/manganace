from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from database import Base


class CImage(Base):
    __tablename__ = "c_images"

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable=False)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)

    collection = relationship("Collection", back_populates="c_images")
    image = relationship("Image", back_populates="c_images")
    tags = relationship("Tag", secondary='c_image_tag', back_populates="c_images")
