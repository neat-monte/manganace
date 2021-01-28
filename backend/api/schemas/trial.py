from typing import List

from fastapi_camelcase import CamelModel
from pydantic import conint, HttpUrl, confloat, constr


class TrialMeta(CamelModel):
    """ Meta information about a single trial """
    session_id: conint(gt=0)
    vector_id: conint(gt=0)
    seed: conint(ge=0, le=4294967295)  # maximum seed number is 2^32 - 1 (because starts at 0)
    emotion: constr(max_length=64)


class TrialImage(CamelModel):
    """ Single image information about  """
    id: conint(gt=0)
    url: HttpUrl
    vector_multiplier: confloat(ge=0, le=1)
