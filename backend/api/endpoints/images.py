from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from api.dependencies import get_db
from schemas import Image, ImageCreate, ImageUpdate
from services import ImageService, ImageFileService

router = APIRouter()


@router.get("/{id_}", response_model=Image)
def get_image(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get an image by id """
    image = ImageService.get_image(db, id_)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post('/', response_model=Image)
def create_image(image_in: ImageCreate, session: Optional[str] = Cookie(None),
                 db: Session = Depends(get_db)) -> Any:
    """ Save a generated image and register image instance """
    if not ImageFileService.image_exists(session, image_in.filename):
        raise HTTPException(status_code=404, detail="Image file not found")
    try:
        image = ImageService.create_image(db, image_in)
    finally:
        ImageFileService.save_image(session, image_in.filename)
    return image


@router.put('/{id_}', response_model=Image)
def update_image(id_: int, image_in: ImageUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing image """
    image = ImageService.update_image(db, id_, image_in)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/{id_}", response_model=Image)
def delete_image(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete an image """
    image = ImageService.delete_image(db, id_)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    ImageFileService.delete_image(db, image.filename)
    return image
