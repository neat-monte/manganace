from typing import List

from fastapi_camelcase import CamelModel
from pydantic import constr


class SingleVectorData(CamelModel):
    effect: constr(max_length=64)
    points: List[float]
