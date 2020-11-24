from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    explanation = Column(String(100), nullable=False)

    participants = relationship("Participant", back_populates="education")
