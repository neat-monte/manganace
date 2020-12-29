from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from database import Base
from ._mixins import Timestamp


class Participant(Base, Timestamp):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    consented = Column(Boolean, default=False)
    consented_on = Column(DateTime, nullable=False)
    age = Column(Integer, nullable=False)
    gender_id = Column(Integer, ForeignKey('genders.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('research_sessions.id'), nullable=False)
    collection_id = Column(Integer, ForeignKey('participant_collections.id'), nullable=False)

    gender = relationship("Gender", back_populates="participants")
    session = relationship("ResearchSession", back_populates="participant")
    collection = relationship("ParticipantCollection", back_populates="participant", cascade="all, delete")
