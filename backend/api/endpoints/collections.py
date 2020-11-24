from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import data
import models as m
import services
from api.dependencies import get_db
from schemas import Collection, CImage, CollectionCreate, CollectionUpdate

router = APIRouter()


@router.get('/user', response_model=List[Collection])
def get_collections(db: Session = Depends(get_db)) -> Any:
    """ Get all user collections """
    return data.collection_u.get_all(db)


@router.get('/user/{id_}', response_model=Collection)
def get_collection(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a user collection by id """
    collection = data.collection_u.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.post('/user', response_model=Collection)
def create_collection(collection_in: CollectionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new user collection """
    return data.collection_u.create(db, collection_in)


@router.put('/user/{id_}', response_model=Collection)
def update_collection(id_: int, collection_in: CollectionUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing user collection """
    collection = data.collection_u.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return data.collection_u.update(db, collection, collection_in)


@router.delete('/user/{id_}', response_model=Collection)
def delete_collection(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a user collection """
    collection = data.collection_u.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    for c_image in collection.c_images:
        data.c_image.delete(db, c_image.id)
    return data.collection_u.delete(db, id_)


@router.get('/{id_}/images', response_model=List[CImage])
def get_collection_images(id_, db: Session = Depends(get_db)) -> Any:
    """ Get all images of a any collection by id """
    collection = db.query(m.Collection).get(id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return services.c_image.get_all_of_collection(db, id_)