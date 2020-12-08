from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class CImageTag(Base):
    __tablename__ = 'c_image_tag'

    c_image_id = Column(Integer, ForeignKey('c_images.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
