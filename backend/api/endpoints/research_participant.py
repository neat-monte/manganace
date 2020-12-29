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


@router.delete('/participants/{id_}', response_model=Participant)
def delete_participant(id_: int, db: Session = Depends(get_db)) -> Any:
    """  Delete a participant with all the data that was gathered. """
    db_participant = CRUD.participant.get(db, id_)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return CRUD.participant.delete(db, id_)
