from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services
from api.dependencies import get_db
from database.models import Collection
from api.schemas import CImage, CImageCreate, CImageUpdate, TrialPickCreate, TrialPick

router = APIRouter()


@router.get("/{id_}", response_model=CImage)
def get_collection_image(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a collection image by id """
    c_image = services.c_image.get(db, id_)
    if not c_image:
        raise HTTPException(status_code=404, detail="Collection image not found")
    return c_image


@router.post('/', response_model=CImage)
def create_collection_image(c_image_in: CImageCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new collection image """
    image = services.image.get(db, c_image_in.image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    db_collection = db.query(Collection).get(c_image_in.collection_id)
    if not db_collection:
        raise HTTPException(status_code=400, detail="Collection not found")
    return services.c_image.create(db, c_image_in)


@router.put('/{id_}', response_model=CImage)
def update_collection_image(id_: int, image_in: CImageUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing collection image """
    c_image = services.c_image.update(db, id_, image_in)
    if not c_image:
        raise HTTPException(status_code=404, detail="Collection image not found")
    return c_image


@router.delete("/{id_}", response_model=CImage)
def delete_collection_image(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a collection image """
    c_image = services.c_image.delete(db, id_)
    if not c_image:
        raise HTTPException(status_code=404, detail="Collection image not found")
    return c_image


@router.post('/trial', response_model=TrialPick)
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
