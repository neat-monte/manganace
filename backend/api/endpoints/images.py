from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import Image, ImageCreate, ImageUpdate
from services import image_service, image_file_service

router = APIRouter()


@router.get("/{id_}", response_model=Image)
def get_image(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Get an image by id """
    image = image_service.get_image(db, id_)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post('/', response_model=Image)
def create_image(image_in: ImageCreate, session: Optional[str] = Cookie(None),
                 db: Session = Depends(deps.get_db)) -> Any:
    """ Save a generated image and register image instance """
    if not image_file_service.image_exists(session, image_in.filename):
        raise HTTPException(status_code=404, detail="Image file not found")
    try:
        image = image_service.create_image(db, image_in)
    finally:
        image_file_service.save_image(session, image_in.filename)
    return image


@router.put('/{id_}', response_model=Image)
def update_image(id_: int, image_in: ImageUpdate, db: Session = Depends(deps.get_db)) -> Any:
    """ Modify an existing image """
    image = image_service.update_image(db, id_, image_in)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/{id_}", response_model=Image)
def delete_image(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Delete an image """
    # image = crud.image.get(db, id_)
    # if not image:
    #     raise HTTPException(status_code=404, detail="Image not found")
    # try:
    image = image_service.delete_image(db, id_)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image_file_service.delete_image(db, image.filename)
    return image
