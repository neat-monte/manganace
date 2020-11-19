from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import data
import services
from api.dependencies import get_db
from schemas import ResearchSessionCreate, ResearchSession
from schemas import Participant, ParticipantCreate

router = APIRouter()


@router.get('/', response_model=List[ResearchSession])
def get_sessions(db: Session = Depends(get_db)):
    """ Get all available research sessions """
    return services.research.get_sessions(db)


@router.post('/', response_model=ResearchSession)
def initialize_session(session_r_in: ResearchSessionCreate, db: Session = Depends(get_db)):
    """ Initialize research session by pre-generating all images with all emotion vectors """
    if not services.generator.is_initialized():
        services.generator.initialize(db)
    db_session_r = data.session_r.create(db, session_r_in)
    services.generator.create_research_trials(db, db_session_r)
    return services.research.get_session_schema(db, db_session_r)


@router.post('/participant', response_model=Participant)
def assign_participant(participant_in: ParticipantCreate, db: Session = Depends(get_db)):
    """ Create participant for a particular session """
    db_session_r = data.session_r.get(db, participant_in.session_id)
    if not db_session_r:
        raise HTTPException(status_code=400, detail="Session not found")
    if db_session_r.participant:
        raise HTTPException(status_code=400, detail="Session already contains a participant")
    return data.participant.create_for_session(db, participant_in, db_session_r)

