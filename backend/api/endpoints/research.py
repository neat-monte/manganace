from typing import List

from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session

import crud
import services
from api.dependencies import get_db
from schemas import ResearchSessionCreate, ResearchSession

router = APIRouter()


@router.get('/', response_model=List[ResearchSession])
def get_sessions(db: Session = Depends(get_db)):
    """ Get all available research sessions """
    return crud.session_r.get_all(db)


@router.post('/', response_model=ResearchSession)
def initialize_session(request: ResearchSessionCreate, db: Session = Depends(get_db)):
    """ Initialize research session by pre-generating all images with all emotion vectors """
    if not services.generator.is_initialized():
        services.generator.initialize(db)
    session = crud.session_r.create(db, request)
    services.generator.create_research_trials(db, session)
    return session


def assign_participant(db: Session = Depends(get_db)):
    """ Create participant for particular session """
    # check if session exists
    # check if participant is not yet assigned
    # create participant
    # assign participant to session
    pass
