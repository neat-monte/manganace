from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import Collection, CollectionCreate, CollectionUpdate
from database import CRUD

router = APIRouter()


@router.get('/user', response_model=List[Collection])
def get_collections(db: Session = Depends(get_db)) -> Any:
    """ Get all user collections """
    return CRUD.user_collection.get_all(db)


@router.post('/user', response_model=Collection)
def create_collection(collection_in: CollectionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new user collection """
    return CRUD.user_collection.create(db, collection_in)


@router.put('/user/{id_}', response_model=Collection)
def update_collection(id_: int, collection_in: CollectionUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing user collection """
    collection = CRUD.user_collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return CRUD.user_collection.update(db, collection, collection_in)


@router.delete('/user/{id_}', response_model=Collection)
def delete_collection(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a user collection """
    collection = CRUD.user_collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    for collection_image in collection.collection_images:
        CRUD.collection_image.delete(db, collection_image.id)
    return CRUD.user_collection.delete(db, id_)
