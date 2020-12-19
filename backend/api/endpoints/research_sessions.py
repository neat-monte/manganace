from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import services
from api.dependencies import get_db
from api.schemas import ResearchSession, ResearchSessionCreate
from database import CRUD

router = APIRouter()


@router.get('/research/{research_setting_id}', response_model=List[ResearchSession])
def get_research_sessions(research_setting_id: int, db: Session = Depends(get_db)) -> Any:
    """ Get a list of research sessions """
    return services.research.get_sessions(db)


@router.post('/research/{research_setting_id}', response_model=ResearchSession)
def create_research_session(research_setting_id: int, research_session_in: ResearchSessionCreate,
                            batch_size: int = 10, db: Session = Depends(get_db)) -> Any:
    """ Create a new research session by pre-generating all images with all emotion vectors \n
        NOTE: this might take a long time! """
    db_research_session = CRUD.research_session.create(db, research_session_in)
    services.generator.create_research_trials(db, db_research_session, batch_size)
    return services.research.get_session_schema(db, db_research_session)