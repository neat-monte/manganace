from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database.models as m
import services
from api.dependencies import get_db
from api.schemas import CImage, CImageCreate, CImageUpdate, TrialPickCreate, TrialPick
from database.models import Collection

router = APIRouter()


@router.get('/{collection_id}/images', response_model=List[CImage])
def get_collection_images(collection_id, db: Session = Depends(get_db)) -> Any:
    """ Get all images of a any collection by id """
    collection = db.query(m.Collection).get(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return services.collection_image.get_all_of_collection(db, collection_id)


@router.post('/images', response_model=CImage)
def create_collection_image(collection_image_in: CImageCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new collection image """
    image = services.image.get(db, collection_image_in.image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db_collection = db.query(Collection).get(collection_image_in.collection_id)
    if not db_collection:
        raise HTTPException(status_code=400, detail="Collection not found")
    return services.collection_image.create(db, collection_image_in)


@router.post('/trial-pick', response_model=TrialPick)
def create_trial_pick(trial_pick_in: TrialPickCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new trial pick """
    image = services.image.get(db, trial_pick_in.image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db_collection = db.query(Collection).get(trial_pick_in.collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    if not db_collection.type == "participant":
        raise HTTPException(status_code=400, detail="Wrong collection type")
    return services.trial_pick.create(db, trial_pick_in)


@router.put('/images/{id_}', response_model=CImage)
def update_collection_image(id_: int, image_in: CImageUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing collection image """
    collection_image = services.collection_image.update(db, id_, image_in)
    if not collection_image:
        raise HTTPException(status_code=404, detail="Collection image not found")
    return collection_image


@router.delete("/images/{id_}", response_model=CImage)
def delete_collection_image(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a collection image """
    collection_image = services.collection_image.delete(db, id_)
    if not collection_image:
        raise HTTPException(status_code=404, detail="Collection image not found")
    return collection_image
