from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    images = relationship("CollectionImage", secondary='collection_image_tag', back_populates="tags")
