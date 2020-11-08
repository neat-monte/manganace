from typing import List, Optional

from fastapi_camelcase import CamelModel
from pydantic import conint, HttpUrl, confloat

from schemas.emotion import Emotion, EmotionMultiplier


class GeneratorInitializedResponse(CamelModel):
    """ Properties that are return after the generator initializes """
    session: str
    emotions: List[Emotion]


class GenerateRequest(CamelModel):
    """ Properties that are expected to generate an image """
    seed: conint(ge=0, lt=4294967296)  # maximum seed number is 2^31 - 1 (because starts from 0)
    emotions: Optional[List[EmotionMultiplier]] = None


class GenerateResponse(GenerateRequest):
    """ Properties that are returned after an image is generated """
    filename: str
    path: HttpUrl


class UnsavedSessionActivityImage(CamelModel):
    """ Properties of unsaved images from session activity that are returned via the API """
    seed: int
    filename: str
    path: HttpUrl
