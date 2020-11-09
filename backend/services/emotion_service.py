from sqlalchemy.orm import Session

import crud
from schemas import Emotion


class EmotionService:
    @staticmethod
    def get_emotions(db: Session):
        emotions_db = crud.emotion.get_all(db)
        emotions = []
        for emotion_db in emotions_db:
            emotion = Emotion.construct(id=emotion_db.id, name=emotion_db.name, weight=emotion_db.weight)
            emotions.append(emotion)
        return emotions

    @staticmethod
    def get_emotions_dict(db: Session):
        emotions_db = crud.emotion.get_all(db)
        name_weight_by_id = {}
        for emotion_db in emotions_db:
            name_weight_by_id[emotion_db.id] = (emotion_db.name, emotion_db.weight)
        return name_weight_by_id
