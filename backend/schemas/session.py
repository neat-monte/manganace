from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic.class_validators import validator
from pydantic.types import conint, constr

from schemas import Participant


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
    total_amount: conint(gt=0)
    overlap_amount: conint(ge=0)
    slider_steps: Optional[conint(ge=2)] = 21
    equalize_gender: bool

    @validator("overlap_amount")
    def validate_overlap(cls, value, values):
        if value > values["total_amount"]:
            raise ValueError("Overlapping amount cannot be larger than total")
        return value


class ResearchSessionInDb(SessionInDb):
    """ Properties that are stored in the database """
    total_amount: conint(gt=0)
    overlap_amount: conint(ge=0)
    equalize_gender: bool
    slider_steps: conint(ge=2)
    created: datetime


class ResearchSession(ResearchSessionInDb):
    """ Properties that are returned via the API """
    trials: conint(ge=0)
    progress: conint(ge=0)  # done trials
    participant: Optional[Participant]
