from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
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
def initialize_session(session_in: ResearchSessionCreate, db: Session = Depends(get_db)):
    """ Initialize research session by pre-generating all images with all emotion vectors """
    if not services.generator.is_initialized():
        services.generator.initialize(db)
    session = crud.session_r.create(db, session_in)
    services.generator.create_research_trials(db, session)
    return services.research.get_session_schema(db, session)


@router.post('/participant', response_model=Participant)
def assign_participant(participant_in: ParticipantCreate, db: Session = Depends(get_db)):
    """ Create participant for particular session """
    # check if session exists
    # check if participant is not yet assigned
    # create participant
    # create participant collection
    # assign collection to participant
    # assign participant to session
    pass
