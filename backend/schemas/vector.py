from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import confloat


class VectorBase(CamelModel):
    """ Properties that are shared """
    id: int


class Vector(VectorBase):
    """ Properties that are returned about possible emotions, it is an essential part of GeneratorInitializeResponse """
    name: str
    effect: str
    min: float = 0
    max: float = 1


class VectorMultiplier(VectorBase):
    """ Properties that are required to apply an emotion vector, it is an essential part of the GenerateRequest """
    multiplier: confloat(ge=0, le=1)
