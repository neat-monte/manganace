from sqlalchemy.orm import Session

import crud
from schemas import Emotion


class EmotionService:
    @staticmethod
    def get_emotions(db: Session):
        emotions_db = crud.emotion.get_all(db)
        emotions = []
        for emotion_db in emotions_db:
            emotion = Emotion.construct(name=emotion_db.name, weight=emotion_db.weight)
            emotions.append(emotion)
        return emotions

    @staticmethod
    def get_emotion_weights(db: Session):
        emotions_db = crud.emotion.get_all(db)
        emotion_weights = {}
        for emotion_db in emotions_db:
            emotion_weights[emotion_db.name] = emotion_db.weight
        return emotion_weights
