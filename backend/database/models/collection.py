from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    c_images = relationship("CImage", back_populates="collection")

    __mapper_args__ = {
        'polymorphic_identity': 'basic',
        'polymorphic_on': type
    }


class UserCollection(Collection, Timestamp):
    __tablename__ = "collections_u"

    id = Column(Integer, ForeignKey('collections.id'), primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }


class ParticipantCollection(Collection, Timestamp):
    __tablename__ = "collections_p"

    id = Column(Integer, ForeignKey('collections.id'), primary_key=True)

    participant = relationship("Participant", back_populates="collection")

    __mapper_args__ = {
        'polymorphic_identity': 'participant',
    }
