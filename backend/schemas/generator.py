from typing import List, Optional

from fastapi_camelcase import CamelModel
from pydantic import conint, HttpUrl, confloat

from schemas.vector import Vector, ImageVector


class GeneratorInitializedResponse(CamelModel):
    """ Properties that are return after the generator initializes """
    vectors: List[Vector]


class GenerateRequest(CamelModel):
    """ Properties that are expected to generate an image """
    session_id: conint(gt=0)
    seed: conint(ge=0, lt=4294967296)  # maximum seed number is 2^31 - 1 (because starts from 0)
    vectors: Optional[List[ImageVector]]
