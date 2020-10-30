import os
import uuid
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, Response, Cookie, HTTPException

from encoder.interface import generator
from schemas import UnsavedSessionActivityImage, GenerateRequest, GenerateResponse, GeneratorInitializedResponse

router = APIRouter()


@router.get('/', response_model=GeneratorInitializedResponse)
def initialize(response: Response, session: Optional[str] = Cookie(None)):
    """ Initializes the generator and provides a session cookie as JSON but also
        within the header which is set automatically in the browser """
    if not generator.is_initialized():
        generator.initialize()
    if not session:
        session = str(uuid.uuid4())
        response.set_cookie(key="session", value=session)
        session_dir = Path.cwd() / 'static' / 'images' / 'sessions' / session
        session_dir.mkdir(parents=True)
    response = GeneratorInitializedResponse.construct(session=session)
    return response


@router.post('/', response_model=GenerateResponse)
def generate(request: GenerateRequest, session: Optional[str] = Cookie(None)):
    """ Generates an image according to the provided request model """
    if not generator.is_initialized():
        return HTTPException(status_code=412, detail="The generator is not initialized")
    image_filename = generator.get_image_by_seed(request.seed, session)
    response = GenerateResponse.construct(**request.dict(), filename=image_filename)
    return response


@router.get('/activity', response_model=List[UnsavedSessionActivityImage])
def get_activity(session: Optional[str] = Cookie(None)):
    """ Gets a list of images already generated in the session, requires a cookie of session in the header """
    if not session:
        return []
    session_dir = Path.cwd() / 'static' / 'images' / 'sessions' / session
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
