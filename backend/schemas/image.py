from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import constr, HttpUrl

from .vector import VectorMultiplier


class ImageBase(CamelModel):
    """ Properties that are shared """
    description: Optional[str] = None
    collection_id: Optional[int] = None


class ImageCreate(ImageBase):
    """ Properties that are available/required for the creation """
    seed: int
    filename: constr(max_length=51)
    collection_id: int
    vectors: Optional[List[VectorMultiplier]]
    tags_ids: Optional[List[int]]


class ImageUpdate(ImageBase):
    """ Properties that are available/required for an update """
    tags_ids: Optional[List[int]]


class ImageInDb(ImageBase):
    """ Properties that are in the database """
    id: int
    seed: int
    filename: constr(max_length=51)
    collection_id: int

    class Config:
        orm_mode = True


class Image(ImageInDb):
    """ Properties without any relations that are returned via the API """
    url: HttpUrl
    vectors: List[VectorMultiplier]
    tags_ids: List[int]
    pass
