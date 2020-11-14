from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import services
from api.dependencies import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.Session])
def get_sessions(db: Session = Depends(get_db)) -> Any:
    """ Get a list of all sessions """
    return crud.session.get_all(db)


@router.get("/{id_}", response_model=schemas.Session)
def get_session(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a session by id """
    session = crud.session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get('/{id_}/images', response_model=List[schemas.CImage])
def get_session_images(id_: int, db: Session = Depends(get_db)):
    """ Gets all images of a session by id """
    session = crud.session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.image.get_all_of_session(db, id_)


@router.post('/', response_model=schemas.Session)
def create_session(session_in: schemas.GeneratorSessionCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new session """
    s = crud.session.create(db, session_in)
    return s


@router.put('/{id_}', response_model=schemas.Session)
def update_session(id_: int, session_in: schemas.GeneratorSessionUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing session """
    session = crud.session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return crud.session.update(db, session, session_in)


@router.delete("/{id_}", response_model=schemas.Session)
def delete_session(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a session """
    session = crud.session.get(db, id_)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return crud.session.delete(db, id_)
