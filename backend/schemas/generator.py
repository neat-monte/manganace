from fastapi_camelcase import CamelModel
from pydantic import conint


class GenerateRequest(CamelModel):
    """ Properties that are expected to generate an image """
    seed: conint(lt=4294967296)


class GenerateResponse(GenerateRequest):
    """ Properties that are returned after an image is generated """
    filename: str
