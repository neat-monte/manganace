from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import HttpUrl, conint

from .vector import ImageVector


class CImageCreate(CamelModel):
    """ Properties that are available/required for the creation """
    collection_id: conint(gt=0)
    image_id: conint(gt=0)
    description: Optional[str]
    tags_ids: Optional[List[int]]


class CImageUpdate(CamelModel):
    """ Properties that are available/required for an update """
    description: Optional[str]
    tags_ids: Optional[List[int]]


class CImage(CamelModel):
    """ Properties that are returned via the API """
    id: conint(gt=0)
    collection_id: conint(gt=0)
    image_id: conint(gt=0)
    session_id: conint(gt=0)
    seed: conint(ge=0, lt=4294967296)
    description: Optional[str]
    tags_ids: List[int]
    url: HttpUrl
    vectors: List[ImageVector]