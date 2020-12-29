from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship

from database import Base


class ResearchSetting(Base):
    __tablename__ = "research_settings"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    total_amount = Column(Integer, nullable=False)
    overlap_amount = Column(Integer, nullable=False)
    equalize_gender = Column(Boolean, default=False)
    slider_steps = Column(Integer, default=21)
    global_multiplier = Column(Float, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)

    research_sessions = relationship("ResearchSession", back_populates="research_setting")
