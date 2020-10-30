from datetime import datetime
from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import constr

from .image import ImageWithTags


class CollectionBase(CamelModel):
    """ Properties that are shared """
    name: Optional[constr(max_length=64)] = None
    description: Optional[str] = None
    is_archived: Optional[bool] = False


class CollectionCreate(CollectionBase):
    """ Properties that are available/required for the creation """
    name: constr(max_length=64)


class CollectionUpdate(CollectionBase):
    """ Properties that are available/required for an update """
    pass


class CollectionInDb(CollectionBase):
    """ Properties that are stored in the database """
    id: int
    name: constr(max_length=64)
    is_archived: bool
    created: datetime
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class Collection(CollectionInDb):
    """ Properties without any relations that are returned via the API """
    pass


class CollectionWithImages(CollectionInDb):
    """ Properties with relations that are returned via the API """
    images: List[ImageWithTags]
