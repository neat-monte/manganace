from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class CollectionImageTag(Base):
    __tablename__ = 'collection_image_tag'

    collection_image_id = Column(Integer, ForeignKey('collection_images.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
