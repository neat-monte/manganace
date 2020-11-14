from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import services
from api.dependencies import get_db
from schemas import Collection, CImage, CollectionCreate, CollectionUpdate

router = APIRouter()


@router.get('/', response_model=List[Collection])
def get_collections(db: Session = Depends(get_db)) -> Any:
    """ Get all collections """
    return crud.collection.get_all(db)


@router.get('/{id_}', response_model=Collection)
def get_collection(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a collection by id """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.get('/{id_}/images', response_model=List[CImage])
def get_collection_images(id_, db: Session = Depends(get_db)) -> Any:
    """ Get all images of a collection by id """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return services.c_image.get_all_of_collection(db, id_)


@router.post('/', response_model=Collection)
def create_collection(collection_in: CollectionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new collection """
    return crud.collection.create(db, collection_in)


@router.put('/{id_}', response_model=Collection)
def update_collection(id_: int, collection_in: CollectionUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing collection """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.collection.update(db, collection, collection_in)


@router.delete('/{id_}', response_model=Collection)
def delete_collection(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a collection """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return crud.collection.delete(db, id_)
