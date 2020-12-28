from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic.types import conint


class ParticipantCreate(CamelModel):
    """ Properties that are available/required for the creation """
    age: conint(gt=0)
    consented: bool
    consented_on: datetime
    gender_id: conint(gt=0)
    session_id: conint(gt=0)


class ParticipantInDb(CamelModel):
    """ Properties that are stored in the database """
    id: conint(gt=0)
    age: conint(gt=0)
    consented: bool
    consented_on: datetime
    gender_id: conint(gt=0)
    session_id: conint(gt=0)
    collection_id: conint(gt=0)
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True


class Participant(ParticipantInDb):
    """ Properties that are returned via the API """
    pass
