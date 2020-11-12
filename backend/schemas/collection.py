from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import constr


class CollectionBase(CamelModel):
    """ Properties that are shared """
    name: Optional[constr(max_length=64)] = None
    description: Optional[str] = None


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
    created: datetime
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class Collection(CollectionInDb):
    """ Properties without any relations that are returned via the API """
    pass
