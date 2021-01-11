from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import services
from api.background_tasks import delete_folder
from api.dependencies import get_db
from api.schemas import ResearchSession, ResearchSessionCreateOrder
from database import CRUD

router = APIRouter()


@router.get('/research/{research_setting_id}', response_model=List[ResearchSession])
def get_research_sessions(research_setting_id: int, db: Session = Depends(get_db)) -> Any:
    """ Get a list of research sessions """
    return services.research.get_sessions(db, research_setting_id)


# noinspection PyBroadException
@router.post('/research/setting', response_model=ResearchSession)
def create_research_session(research_session_order: ResearchSessionCreateOrder,
                            background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    """ Create a new research session by pre-generating all images with all emotion vectors \n
        NOTE: this might take a long time! """
    db_research_session = CRUD.research_session.create(db, research_session_order.session)
    try:
        services.generator.create_research_trials(db, db_research_session, research_session_order.batch_size)
    except Exception:
        filepath = services.image_file.get_folder_path(db_research_session.id)
        background_tasks.add_task(delete_folder, filepath=filepath)
        CRUD.research_session.delete(db, db_research_session.id)
        raise HTTPException(status_code=500, detail="Generation failed, session creation reversed")
    return services.research.get_session_schema(db, db_research_session)


@router.delete('/research/setting/{research_session_id}', response_model=ResearchSession)
def delete_research_session(research_session_id: int, background_tasks: BackgroundTasks,
                            db: Session = Depends(get_db)) -> Any:
    """ Delete a research session with all the images that belongs to it.
        The session must not contain a participant. """
    db_research_session = CRUD.research_session.get(db, research_session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Research session not found")
    if db_research_session.participant:
        raise HTTPException(status_code=403, detail="Research session contains a participant")
    schema = services.research.get_session_schema(db, db_research_session)
    CRUD.research_session.delete(db, research_session_id)
    filepath = services.image_file.get_folder_path(research_session_id)
    background_tasks.add_task(delete_folder, filepath=filepath)
    return schema
