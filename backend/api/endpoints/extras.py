from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import models
from api.dependencies import get_db
from api.schemas import Gender

router = APIRouter()


@router.get("/genders", response_model=List[Gender])
def get_genders_options(db: Session = Depends(get_db)) -> Any:
    """ Get a list of available gender options """
    return [g.__dict__ for g in db.query(models.Gender).all()]
