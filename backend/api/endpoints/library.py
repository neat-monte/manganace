from typing import List, Any
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from api import deps
from schemas import JustCollection, JustImage

router = APIRouter()


@router.get('/collections', response_model=List[JustCollection])
def get_only_collections(db: Session = Depends(deps.get_db)) -> Any:
    return crud.collection.get_all(db)


@router.get('/collections/{collection_id}/images', response_model=List[JustImage])
def get_collection_images(collection_id, db: Session = Depends(deps.get_db)) -> Any:
    return crud.image.get_images_of(db, collection_id)


