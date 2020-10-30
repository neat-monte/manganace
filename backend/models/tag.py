from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.setup import Base
from .associations import ImageTag


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    images = relationship("Image", secondary='image_tag', back_populates="tags")
    # images = relationship("image_tag", backref="tag", primaryjoin=id == ImageTag.tag_id)
