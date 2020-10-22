from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import Image, ImageCreate, ImageUpdate

router = APIRouter()


@router.post('/', response_model=Image)
def create_image(image_in: ImageCreate, db: Session = Depends(deps.get_db)) -> Any:
    """ Create a new image """
    return crud.image.create_with_tags(db, image_in)


@router.get('/', response_model=List[Image])
def get_images(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)) -> Any:
    """ Get a limited list of images """
    return crud.image.get_multi(db, skip, limit)


@router.get("/{id_}", response_model=Image)
def get_image(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Get an image by id """
    image = crud.image.get(db, id_)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.put('/{id_}', response_model=Image)
def update_image(id_: int, image_in: ImageUpdate, db: Session = Depends(deps.get_db)) -> Any:
    """ Modify an existing image """
    return crud.image.update(db, id_, image_in)


@router.delete("/{id_}", response_model=Image)
def delete_image(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Delete an image """
    item = crud.image.get(db, id_)
    if not item:
        raise HTTPException(status_code=404, detail="Image not found")
    item = crud.image.remove(db, id_)
    return item
