from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    option = Column(String(100), nullable=False)

    participants = relationship("Participant", back_populates="gender")
