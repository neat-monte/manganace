from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    gender_id = Column(Integer, ForeignKey('genders.id'))
    session_id = Column(Integer, ForeignKey('research_sessions.id'))
    collection_id = Column(Integer, ForeignKey('participant_collections.id'))

    gender = relationship("Gender", back_populates="participants")
    session = relationship("ResearchSession", back_populates="participant")
    collection = relationship("ParticipantCollection", back_populates="participant")
