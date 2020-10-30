from sqlalchemy import Column, Integer, ForeignKey, Table

from database.setup import Base


class ImageTag(Base):
    __tablename__ = 'image_tag'

    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
