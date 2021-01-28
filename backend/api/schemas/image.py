from typing import List

from fastapi_camelcase import CamelModel
from pydantic import HttpUrl
from pydantic.types import conint

from api.schemas import ImageVector


class Image(CamelModel):
    """ Properties that are returned via the API """
    id: conint(gt=0)
    seed: conint(ge=0, le=4294967295)  # maximum seed number is 2^32 - 1 (because at from 0)
    session_id: conint(gt=0)
    url: HttpUrl
    vectors: List[ImageVector]
