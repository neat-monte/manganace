from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic.types import conint, constr


class SessionInDb(CamelModel):
    """ Properties that are stored in the database """
    id: conint(gt=0)
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class Session(SessionInDb):
    """ Properties that are returned via the API """
    pass


class GeneratorSessionCreate(CamelModel):
    """ Properties that are available/required for the creation """
    name: constr(max_length=64)


class GeneratorSessionUpdate(CamelModel):
    """ Properties that are available/required for an update """
    id: conint(gt=0)
    name: Optional[constr(max_length=64)]


class GeneratorSessionInDb(SessionInDb):
    """ Properties that are stored in the database """
    name: constr(max_length=64)


class GeneratorSession(GeneratorSessionInDb):
    """ Properties that are returned via the API """
    pass
