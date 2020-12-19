from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import models as m, CRUD
from api.schemas import GeneratorSession, Image, GeneratorSessionCreate, GeneratorSessionUpdate, ResearchSession, \
    ResearchSessionCreate
import services
from api.dependencies import get_db

router = APIRouter()


@router.get('/generator/', response_model=List[GeneratorSession])
def get_generator_sessions(db: Session = Depends(get_db)) -> Any:
    """ Get a list of generator sessions """
    return CRUD.generator_session.get_all(db)


@router.get("/generator/{id_}", response_model=GeneratorSession)
def get_generator_session(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a generator session by id """
    session = CRUD.generator_session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Generator session not found")
    return session


@router.post('/generator/', response_model=GeneratorSession)
def create_generator_session(session_in: GeneratorSessionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new session """
    s = CRUD.generator_session.create(db, session_in)
    return s


@router.put('/generator/{id_}', response_model=GeneratorSession)
def update_generator_session(id_: int, session_in: GeneratorSessionUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing session """
    session = CRUD.generator_session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Generator session not found")
    return CRUD.generator_session.update(db, session, session_in)


@router.delete("/generator/{id_}", response_model=GeneratorSession)
def delete_generator_session(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a session """
    session = CRUD.generator_session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Generator session not found")
    return CRUD.generator_session.delete(db, id_)


@router.get('/research', response_model=List[ResearchSession])
def get_research_sessions(db: Session = Depends(get_db)) -> Any:
    """ Get a list of research sessions """
    return services.research.get_sessions(db)


@router.post('/research', response_model=ResearchSession)
def create_research_session(research_session_in: ResearchSessionCreate,
                            batch_size: int = 10, db: Session = Depends(get_db)) -> Any:
    """ Create a new research session by pre-generating all images with all emotion vectors \n
        NOTE: this might take a long time! """
    db_research_session = CRUD.research_session.create(db, research_session_in)
    services.generator.create_research_trials(db, db_research_session, batch_size)
    return services.research.get_session_schema(db, db_research_session)


@router.get('/{id_}/images', response_model=List[Image])
def get_session_images(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Gets all images of any session by id """
    session = db.query(m.Session).get(id_)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.image.get_all_of_session(db, id_)
