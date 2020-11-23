from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import data
import services
from api.dependencies import get_db
from schemas import Participant, ParticipantCreate, TrialImage, SingleVectorData
from schemas import TrialMeta

router = APIRouter()


@router.post('/participant', response_model=Participant)
def assign_participant(participant_in: ParticipantCreate, db: Session = Depends(get_db)) -> Any:
    """ Create participant for a particular session """
    db_session_r = data.session_r.get(db, participant_in.session_id)
    if not db_session_r:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_session_r.participant:
        raise HTTPException(status_code=400, detail="Session already contains a participant")
    return data.participant.create_for_session(db, participant_in, db_session_r)


@router.get('/{session_r_id}/trials', response_model=List[TrialMeta])
def get_trials_meta_info(session_r_id: int, done: bool = False, db: Session = Depends(get_db)) -> Any:
    """ Get meta information of trials for the research session by providing session id.
        By default, returns trials that need to be done. Set 'done' to true if all trials are needed.  """
    db_session_r = data.session_r.get(db, session_r_id)
    if not db_session_r:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_trials_meta(db, db_session_r, done)


@router.post('/trial-images', response_model=List[TrialImage])
def request_trial_images(meta: TrialMeta, db: Session = Depends(get_db)) -> Any:
    """ Get images list for a single trial by providing trial meta information """
    db_session_r = data.session_r.get(db, meta.session_id)
    if not db_session_r:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_trial_images(db, meta)


@router.get('/data', response_model=List[SingleVectorData])
def get_data(db: Session = Depends(get_db)) -> Any:
    return services.research.get_results_data(db)


@router.get('/data/export')
def export_data_csv(db: Session = Depends(get_db)) -> Any:
    return FileResponse(services.research.export_results_data(db))


@router.get('/data/{session_r_id}', response_model=List[SingleVectorData])
def get_data(session_r_id: int, db: Session = Depends(get_db)) -> Any:
    db_session_r = data.session_r.get(db, session_r_id)
    if not db_session_r:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_results_data(db, session_r_id)
