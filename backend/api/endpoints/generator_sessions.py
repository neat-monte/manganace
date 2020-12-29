from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import services
from api.background_tasks import delete_folder
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
    return CRUD.generator_session.create(db, session_in)


@router.delete('/generator/{generator_session_id}', response_model=GeneratorSession)
def delete_generator_session(generator_session_id: int, background_tasks: BackgroundTasks,
                             db: Session = Depends(get_db)) -> Any:
    """ Delete a generator session with all the images that belong to it.
        The session must not have any collection images saved from it. """
    db_generator_session = CRUD.generator_session.get(db, generator_session_id)
    if not db_generator_session:
        raise HTTPException(status_code=404, detail="Generator session not found")
    for image in db_generator_session.images:
        if image.collection_images:
            raise HTTPException(status_code=403,
                                detail="Generator session contains images used in at least one collection.")
    filepath = services.image_file.get_folder_path(generator_session_id)
    background_tasks.add_task(delete_folder, filepath=filepath)
    return CRUD.generator_session.delete(db, generator_session_id)
