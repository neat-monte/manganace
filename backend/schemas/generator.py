from fastapi_camelcase import CamelModel
from pydantic import conint, HttpUrl


class GeneratorInitializedResponse(CamelModel):
    """ Properties that are return after the generator initializes """
    session: str


class GenerateRequest(CamelModel):
    """ Properties that are expected to generate an image """
    seed: conint(lt=4294967296)


class GenerateResponse(GenerateRequest):
    """ Properties that are returned after an image is generated """
    filename: str
    path: HttpUrl


class UnsavedSessionActivityImage(CamelModel):
    """ Properties of unsaved images from session activity that are returned via the API """
    seed: int
    filename: str
    path: HttpUrl
