from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import GeneratorSession, GeneratorSessionCreate
from database import CRUD

router = APIRouter()


@router.get('/generator', response_model=List[GeneratorSession])
def get_generator_sessions(db: Session = Depends(get_db)) -> Any:
    """ Get a list of generator sessions """
    return CRUD.generator_session.get_all(db)


@router.post('/generator', response_model=GeneratorSession)
def create_generator_session(session_in: GeneratorSessionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new session """
    s = CRUD.generator_session.create(db, session_in)
    return s
