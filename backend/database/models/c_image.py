from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship

from database import Base


class CImage(Base):
    __tablename__ = "c_images"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    description = Column(Text)
    collection_id = Column(Integer, ForeignKey('collections.id'), nullable=False)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)

    collection = relationship("UserCollection", back_populates="c_images")
    image = relationship("Image", back_populates="c_images")
    tags = relationship("Tag", secondary='c_image_tag', back_populates="c_images")

    __mapper_args__ = {
        'polymorphic_identity': 'user saved',
        'polymorphic_on': type
    }


class TrialPick(CImage):
    __tablename__ = "trial_picks"

    id = Column(Integer, ForeignKey('c_images.id'), primary_key=True)
    trial_number = Column(Integer, nullable=False)
    initial_multiplier = Column(Float, nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)

    collection = relationship("ParticipantCollection", back_populates="trial_picks")

    __mapper_args__ = {
        'polymorphic_identity': 'trial choice',
    }
