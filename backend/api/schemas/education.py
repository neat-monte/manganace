from fastapi_camelcase import CamelModel
from pydantic.types import conint, constr


class EducationInDb(CamelModel):
    id: conint(gt=0)
    name: constr(max_length=64)
    explanation: constr(max_length=100)


class Education(EducationInDb):
    pass
