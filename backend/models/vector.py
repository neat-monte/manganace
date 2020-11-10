from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Vector(Base):
    __tablename__ = "vectors"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    effect = Column(String(64), nullable=False)
    weight = Column(Float, nullable=False)

    images = relationship("Image", secondary='image_vectors', back_populates="vectors")
