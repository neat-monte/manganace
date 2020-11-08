import json
from pathlib import Path

from sqlalchemy.orm import Session

from models.emotion import Emotion
from . import LocalSession, Base, engine

SETUP_DATA = Path.cwd() / "_preexisting_data"
EMOTIONS = SETUP_DATA / "emotions.json"


def database_setup():
    """ Create database with tables and populate or update it """
    Base.metadata.create_all(bind=engine)
    db = LocalSession()
    try:
        populate_emotions(db)
    finally:
        db.close()


def populate_emotions(db: Session):
    """ Read the JSON file and populate emotions table or update weights """
    with open(EMOTIONS, "r") as file:
        emotions = json.loads(file.read())
    for emotion in emotions:
        emotion_db = db.query(Emotion).filter(Emotion.name == emotion["name"]).first()
        if emotion_db:
            if emotion_db.weight != emotion["weight"]:
                emotion_db.weight = emotion["weight"]
            continue
        db.add(Emotion(**emotion))
    db.commit()
