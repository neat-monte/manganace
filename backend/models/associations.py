from sqlalchemy import Column, Integer, ForeignKey, Table

from database.setup import Base

image_tag_table = Table('image_tag', Base.metadata,
                        Column('image_id', Integer, ForeignKey('images.id')),
                        Column('tag_id', Integer, ForeignKey('tags.id')))
