from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class ImageVector(Base):
    __tablename__ = 'image_vectors'

    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    vector_id = Column(Integer, ForeignKey('vectors.id'), primary_key=True)
    multiplier = Column(Float, nullable=False)

    image = relationship("Image", back_populates="vectors")
    vector = relationship("Vector", back_populates="images")
