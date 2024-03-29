from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    for_research = Column(Boolean, default=False)

    collection_images = relationship("CollectionImage", secondary='collection_image_tag', back_populates="tags")
