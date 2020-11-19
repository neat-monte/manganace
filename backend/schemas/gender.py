from fastapi_camelcase import CamelModel
from pydantic.types import conint, constr


class GenderInDb(CamelModel):
    id: conint(gt=0)
    name: constr(max_length=64)
    option: constr(max_length=100)


class Gender(GenderInDb):
    pass
