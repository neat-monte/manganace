from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import Collection, CollectionCreate, CollectionUpdate

router = APIRouter()


@router.post('/', response_model=Collection)
def create_collection(collection_in: CollectionCreate, db: Session = Depends(deps.get_db)) -> Any:
    """ Create a new collection """
    return crud.collection.create(db, collection_in)


@router.get('/', response_model=List[Collection])
def get_collections(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)) -> Any:
    """ Get a limited list of collections """
    return crud.collection.get_multi(db, skip, limit)


@router.get('/{id_}', response_model=Collection)
def get_collection(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Get a collection by id """
    collection = crud.collection.get(db, id_)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.put('/{id_}', response_model=Collection)
def update_collection(id_: int, collection_in: CollectionUpdate, db: Session = Depends(deps.get_db)) -> Any:
    """ Modify an existing collection """
    return crud.collection.update(db, id_, collection_in)


@router.delete('/{id_}', response_model=Collection)
def delete_collection(id_: int, db: Session = Depends(deps.get_db)) -> Any:
    """ Delete a collection """
    item = crud.collection.get(db, id_)
    if not item:
        raise HTTPException(status_code=404, detail="Collection not found")
    item = crud.collection.remove(db, id_)
    return item
