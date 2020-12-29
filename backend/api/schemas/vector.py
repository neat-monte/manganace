from fastapi_camelcase import CamelModel
from pydantic import constr, conint


class Vector(CamelModel):
    """ Properties that are returned about possible emotions,
        it is an essential part of GeneratorInitializeResponse """
    id: conint(gt=0)
    name: constr(max_length=64)
    effect: constr(max_length=64)


class ImageVector(CamelModel):
    """ Properties that are required to apply an emotion vector,
        it is an essential part of the GenerateRequest """
    id: conint(gt=0)
    multiplier: float
