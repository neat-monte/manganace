from fastapi_camelcase import CamelModel
from pydantic import constr, conint


class TagCreate(CamelModel):
    """ Properties that are available/required for the creation """
    name: constr(max_length=32)


class TagUpdate(CamelModel):
    """ Properties that are available/required for an update """
    name: constr(max_length=32)


class TagInDb(CamelModel):
    """ Properties that are in the database """
    id: conint(gt=0)
    name: constr(max_length=32)
    for_research: bool

    class Config:
        orm_mode = True


class Tag(TagInDb):
    """ Properties that are returned via the API """
    pass
