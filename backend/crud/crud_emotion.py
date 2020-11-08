from crud.base import CRUDBase
from models import Emotion


class CRUDEmotion(CRUDBase[Emotion, None, None]):
    pass


emotion = CRUDEmotion(Emotion)
