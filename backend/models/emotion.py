from sqlalchemy import Column, Integer, String, Float

from database import Base


class Emotion(Base):
    __tablename__ = "emotions"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    weight = Column(Float, nullable=False)
