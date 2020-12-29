from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'basic',
        'polymorphic_on': type
    }


class UserCollection(Collection, Timestamp):
    __tablename__ = "user_collections"

    id = Column(Integer, ForeignKey('collections.id'), primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(Text)

    collection_images = relationship("CollectionImage", back_populates="collection", cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }


class ParticipantCollection(Collection, Timestamp):
    __tablename__ = "participant_collections"

    id = Column(Integer, ForeignKey('collections.id'), primary_key=True)

    participant = relationship("Participant", back_populates="collection")
    trial_picks = relationship("TrialPick", back_populates="collection", cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'participant',
    }
