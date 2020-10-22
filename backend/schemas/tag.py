from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import constr


class TagBase(CamelModel):
    """ Properties that are shared """
    name: Optional[constr(max_length=32)] = None


class TagCreate(TagBase):
    """ Properties that are available/required for the creation """
    name: constr(max_length=32)


class TagUpdate(TagBase):
    """ Properties that are available/required for an update """
    id: int
    name: constr(max_length=32)


class TagInDb(TagBase):
    """ Properties that are in the database """
    id: int
    name: constr(max_length=32)

    class Config:
        orm_mode = True


class Tag(TagInDb):
    """ Properties that are returned via the API """
    pass
