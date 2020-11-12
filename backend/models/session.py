from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Session(Base, Timestamp):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    images = relationship("Image", back_populates="session")

    __mapper_args__ = {
        'polymorphic_identity': 'basic',
        'polymorphic_on': type
    }


class GeneratorSession(Session):
    __tablename__ = "generator_sessions"

    id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    name = Column(String(64), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'generator',
    }
