from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import services
from api.dependencies import get_db
from schemas import GenerateRequest, GeneratorInitializedResponse, Image

router = APIRouter()


@router.get('/', response_model=GeneratorInitializedResponse)
def initialize(db: Session = Depends(get_db)):
    """ Initializes the generator and returns available vectors list """
    if not services.generator.is_initialized():
        services.generator.initialize(db)
    return GeneratorInitializedResponse.construct(vectors=services.vector.get_vectors(db))


@router.post('/', response_model=Image)
def generate(request: GenerateRequest, db: Session = Depends(get_db)):
    """ Generates an image according to the provided request model """
    if not services.generator.is_initialized():
        return HTTPException(status_code=412, detail="The generator is not initialized")
    session = crud.session.get(db, request.session_id)
    if not session:
        return HTTPException(status_code=404, detail="Session not found")
    image_filename = services.generator.generate_image(request)
    return services.image.create(db, request, image_filename)
