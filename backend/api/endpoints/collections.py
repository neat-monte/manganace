from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import Collection, Image, CollectionCreate, CollectionUpdate
from services import ImageService

router = APIRouter()


@router.get('/', response_model=List[Collection])
def get_collections(db: Session = Depends(deps.get_db)) -> Any:
    return crud.collection.get_all(db)


@router.get('/{id_}', response_model=Collection)
def get_collection(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Get a collection by id """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.get('/{id_}/images', response_model=List[Image])
def get_collection_images(id_, db: Session = Depends(deps.get_db)) -> Any:
    """ Get all images of a collection by id """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return ImageService.get_images_of_collection(db, id_)


# @router.get('/', response_model=List[Image])
# def get_images(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)) -> Any:
#     """ Get a limited list of images """
#     return crud.image.get_multi(db, skip, limit)


@router.post('/', response_model=Collection)
def create_collection(collection_in: CollectionCreate, db: Session = Depends(deps.get_db)) -> Any:
    """ Create a new collection """
    return crud.collection.create(db, collection_in)


@router.put('/{id_}', response_model=Collection)
def update_collection(id_: int, collection_in: CollectionUpdate, db: Session = Depends(deps.get_db)) -> Any:
    """ Modify an existing collection """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.collection.update(db, collection, collection_in)


@router.delete('/{id_}', response_model=Collection)
def delete_collection(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Delete a collection """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.collection.remove(db, id_)
