import shutil
from pathlib import Path
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, Cookie, Response
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import JustCollection, JustImage, Image, ImageCreate

router = APIRouter()


@router.get('/collections', response_model=List[JustCollection])
def get_only_collections(db: Session = Depends(deps.get_db)) -> Any:
    return crud.collection.get_all(db)


@router.get('/collections/{collection_id}/images', response_model=List[JustImage])
def get_collection_images(collection_id, db: Session = Depends(deps.get_db)) -> Any:
    return crud.image.get_images_of(db, collection_id)


@router.post('/images', response_model=Image)
def create_image(image_in: ImageCreate, session: Optional[str] = Cookie(None), db: Session = Depends(deps.get_db)) -> Any:
    image_loc = Path.cwd() / 'static' / 'images' / 'session' / session / image_in.filename
    if not image_loc.exists():
        return Response(status_code=404)
    try:
        image = crud.image.create_with_tags(db, image_in)
    finally:
        new_loc = Path.cwd() / 'static' / 'images' / 'saved' / image_in.filename
        shutil.copy(image_loc, new_loc)
    return image
