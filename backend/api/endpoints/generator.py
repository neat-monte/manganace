import os
import uuid
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, Response, Cookie

from encoder.interface import generator
from schemas import UnsavedSessionActivityImage
from schemas.generator import GenerateRequest, GenerateResponse

router = APIRouter()


@router.get('/')
def initialize(response: Response, session: Optional[str] = Cookie(None)):
    if not generator.is_initialized():
        generator.initialize()
    if not session:
        session = str(uuid.uuid4())
        response.set_cookie(key="session", value=session)
        session_dir = Path.cwd() / 'static' / 'images' / 'session' / session
        session_dir.mkdir(parents=True)
    response.status_code = 200
    return response


@router.post('/', response_model=GenerateResponse)
def generate(request: GenerateRequest, session: Optional[str] = Cookie(None)):
    if not generator.is_initialized():
        return Response(status_code=412)
    image_filename = generator.get_image_by_seed(request.seed, session)
    response = GenerateResponse.construct(**request.dict(), filename=image_filename)
    return response


@router.get('/activity', response_model=List[UnsavedSessionActivityImage])
def get_activity(session: Optional[str] = Cookie(None)):
    if not session:
        return []
    session_dir = Path.cwd() / 'static' / 'images' / 'session' / session
    contents = session_dir.glob('**/*')
    files = [x for x in contents if x.is_file()]
    files.sort(key=os.path.getctime, reverse=True)
    images = []
    for file in files:
        filename = file.name
        seed = int(filename.split('_')[0])
        image = UnsavedSessionActivityImage.construct(seed=seed, filename=filename)
        images.append(image)
    return images
