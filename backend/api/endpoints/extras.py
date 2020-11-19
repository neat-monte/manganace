from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from api.dependencies import get_db
from schemas import Gender, Education

router = APIRouter()


@router.get("/genders", response_model=List[Gender])
def get_genders_options(db: Session = Depends(get_db)) -> Any:
    """ Get a list of available gender options """
    return [g.__dict__ for g in db.query(models.Gender).all()]


@router.get("/educations", response_model=List[Education])
def get_educations_options(db: Session = Depends(get_db)) -> Any:
    """ Get a list of available education options """
    return [e.__dict__ for e in db.query(models.Education).all()]
