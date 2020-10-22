from fastapi import APIRouter
from fastapi.responses import FileResponse

from encoder.interface import generator

router = APIRouter()


@router.get('/generate/{seed}')
async def generate(seed: int):
    if not generator.is_initialized():
        generator.initialize()
    image_loc = generator.get_image_by_seed(seed)
    return FileResponse(image_loc)
