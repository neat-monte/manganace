from datetime import datetime
from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic.class_validators import validator
from pydantic.types import conint, confloat, constr


class ResearchSettingCreate(CamelModel):
    """ Properties that are available/required for the creation """
    name: constr(max_length=64)
    total_amount: conint(gt=0)
    overlap_amount: conint(ge=0)
    slider_steps: Optional[conint(ge=2)] = 21
    equalize_gender: bool
    global_multiplier: confloat(ge=0.001)

    @validator("overlap_amount")
    def validate_overlap(cls, value, values):
        if value > values["total_amount"]:
            raise ValueError("Overlapping amount cannot be larger than total")
        return value


class ResearchSettingInDb(CamelModel):
    """ Properties that are stored in the database """
    id: conint(gt=0)
    name: constr(max_length=64)
    total_amount: conint(gt=0)
    overlap_amount: conint(ge=0)
    equalize_gender: bool
    slider_steps: Optional[conint(ge=2)] = 21
    global_multiplier: confloat(ge=0.001)
    created: datetime

    class Config:
        orm_mode = True


class ResearchSetting(ResearchSettingInDb):
    """ Properties that are returned via the API """
    pass
