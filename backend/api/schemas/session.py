from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic.class_validators import validator
from pydantic.types import conint, constr

from api.schemas import Participant


class SessionInDb(CamelModel):
    """ Properties that are stored in the database """
    id: conint(gt=0)

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
    created: datetime
    updated: Optional[datetime]


class GeneratorSession(GeneratorSessionInDb):
    """ Properties that are returned via the API """
    pass


class ResearchSessionCreate(CamelModel):
    """ Properties that are required for the research session initialization """
    research_setting_id: conint(gt=0)


class ResearchSessionCreateOrder(CamelModel):
    batch_size: conint(gt=0)
    session: ResearchSessionCreate


class ResearchSessionInDb(SessionInDb):
    """ Properties that are stored in the database """
    id: conint(gt=0)
    research_setting_id: conint(gt=0)
    created: datetime


class ResearchSession(ResearchSessionInDb):
    """ Properties that are returned via the API """
    trials: conint(ge=0)
    progress: conint(ge=0)  # done trials
    participant: Optional[Participant]
