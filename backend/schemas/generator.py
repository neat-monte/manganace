from typing import List, Optional

from fastapi_camelcase import CamelModel
from pydantic import conint, HttpUrl, confloat

from schemas.vector import Vector, VectorMultiplier


class GeneratorInitializedResponse(CamelModel):
    """ Properties that are return after the generator initializes """
    session: str
    vectors: List[Vector]


class GenerateRequest(CamelModel):
    """ Properties that are expected to generate an image """
    seed: conint(ge=0, lt=4294967296)  # maximum seed number is 2^31 - 1 (because starts from 0)
    vectors: Optional[List[VectorMultiplier]] = None


class GenerateResponse(GenerateRequest):
    """ Properties that are returned after an image is generated """
    filename: str
    url: HttpUrl


class UnsavedSessionActivityImage(CamelModel):
    """ Properties of unsaved images from session activity that are returned via the API """
    seed: int
    filename: str
    url: HttpUrl
