from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import confloat


class EmotionBase(CamelModel):
    """ Properties that are shared """
    id: int
    name: str


class Emotion(EmotionBase):
    """ Properties that are returned about possible emotions, it is an essential part of GeneratorInitializeResponse """
    min: float = 0
    max: float = 1


class EmotionMultiplier(EmotionBase):
    """ Properties that are required to apply an emotion vector, it is an essential part of the GenerateRequest """
    name: Optional[str] = None
    multiplier: confloat(ge=0, le=1)
