import os
import uuid
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, Response, Cookie, HTTPException, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db
from schemas import UnsavedSessionActivityImage, GenerateRequest, GenerateResponse, GeneratorInitializedResponse
from services import ImageFileService, GeneratorService, VectorService

router = APIRouter()


@router.get('/', response_model=GeneratorInitializedResponse)
def initialize(response: Response, session: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """ Initializes the generator and provides a session cookie as JSON but also
        within the header which is set automatically in the browser """
    if not GeneratorService.is_initialized():
        GeneratorService.initialize(db)
    if not session:
        session = str(uuid.uuid4())
        response.set_cookie(key="session", value=session, expires=2**31)
    session_dir = Path.cwd() / 'static' / 'images' / 'sessions' / session
    if not session_dir.exists():
        session_dir.mkdir(parents=True)
    vectors = VectorService.get_vectors(db)
    response = GeneratorInitializedResponse.construct(session=session, vectors=vectors)
    return response


@router.post('/', response_model=GenerateResponse)
def generate(request: GenerateRequest, session: Optional[str] = Cookie(None)):
    """ Generates an image according to the provided request model """
    if not GeneratorService.is_initialized():
        return HTTPException(status_code=412, detail="The generator is not initialized")
    image_filename = GeneratorService.generate_image(request, session)
    url = ImageFileService.make_image_url(image_filename, session)
    response = GenerateResponse.construct(**request.dict(), filename=image_filename, url=url)
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
        url = ImageFileService.make_image_url(filename, session)
        image = UnsavedSessionActivityImage.construct(seed=seed, filename=filename, url=url)
        images.append(image)
    return images
