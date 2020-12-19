from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import Participant, ParticipantCreate
from database import CRUD

router = APIRouter()


@router.post('/participants', response_model=Participant)
def assign_participant(participant_in: ParticipantCreate, db: Session = Depends(get_db)) -> Any:
    """ Create participant for a particular session """
    db_research_session = CRUD.research_session.get(db, participant_in.session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if db_research_session.participant:
        raise HTTPException(status_code=400, detail="Session already contains a participant")
    return CRUD.participant.create_for_session(db, participant_in, db_research_session)
