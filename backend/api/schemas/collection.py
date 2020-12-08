from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import constr, conint


class CollectionCreate(CamelModel):
    """ Properties that are available/required for the creation """
    name: constr(max_length=64)
    description: Optional[str]


class CollectionUpdate(CamelModel):
    """ Properties that are available/required for an update """
    name: Optional[constr(max_length=64)]
    description: Optional[str]


class CollectionInDb(CamelModel):
    """ Properties that are stored in the database """
    id: conint(gt=0)
    name: constr(max_length=64)
    description: Optional[str]
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class Collection(CollectionInDb):
    """ Properties that are returned via the API """
    pass
