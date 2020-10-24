from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import constr

from .tag import Tag


class ImageBase(CamelModel):
    """ Properties that are shared """
    description: Optional[str] = None
    collection_id: Optional[int] = None


class ImageCreate(ImageBase):
    """ Properties that are available/required for the creation """
    seed: int
    filename: constr(max_length=64)
    collection_id: int
    tags_ids: Optional[List[int]] = None


class ImageUpdate(ImageBase):
    """ Properties that are available/required for an update """
    tags_ids: Optional[List[int]] = None


class ImageInDb(ImageBase):
    """ Properties that are in the database """
    id: int
    seed: int
    filename: constr(max_length=64)
    collection_id: int

    class Config:
        orm_mode = True


class Image(ImageInDb):
    """ Properties that are returned via the API """
    tags: List[Tag]


class JustImage(ImageInDb):
    """ Properties without any relations that are returned via the API """
    tags_ids: str
    pass
