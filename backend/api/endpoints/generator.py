from fastapi import APIRouter, Response
from fastapi.responses import FileResponse

from encoder.interface import generator
from schemas.generator import GenerateRequest, GenerateResponse

router = APIRouter()


@router.get('/')
def initialize():
    if not generator.is_initialized():
        generator.initialize()
    return Response(status_code=200)


@router.post('/', response_model=GenerateResponse)
def generate(request: GenerateRequest):
    if not generator.is_initialized():
        return Response(status_code=412)
    image_filename = generator.get_image_by_seed(request.seed)
    response = GenerateResponse.construct(**request.dict(), filename=image_filename)
    return response
