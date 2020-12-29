from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services
from api.dependencies import get_db
from api.schemas import TrialImage
from api.schemas import TrialMeta
from database import CRUD

router = APIRouter()


@router.get('/{research_session_id}/trials', response_model=List[TrialMeta])
def get_trials_meta_info(research_session_id: int, done: bool = False, db: Session = Depends(get_db)) -> Any:
    """ Get meta information of trials for the research session by providing session id.
        By default, returns trials that need to be done. Set 'done' to true if all trials are needed.  """
    db_research_session = CRUD.research_session.get(db, research_session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_trials_meta(db, db_research_session, done)


@router.post('/trial/images', response_model=List[TrialImage])
def get_trial_images(meta: TrialMeta, db: Session = Depends(get_db)) -> Any:
    """ Get images list for a single trial by providing trial meta information """
    db_research_session = CRUD.research_session.get(db, meta.session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_trial_images(db, meta)
