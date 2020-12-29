from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    images = relationship("Image", back_populates="session", cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': 'basic',
        'polymorphic_on': type
    }


class GeneratorSession(Session, Timestamp):
    __tablename__ = "generator_sessions"

    id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    name = Column(String(64), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'generator',
    }


class ResearchSession(Session):
    __tablename__ = "research_sessions"

    id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    research_setting_id = Column(Integer, ForeignKey('research_settings.id'), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)

    research_setting = relationship("ResearchSetting", back_populates="research_sessions")
    participant = relationship("Participant", uselist=False, back_populates="session")

    __mapper_args__ = {
        'polymorphic_identity': 'research',
    }
