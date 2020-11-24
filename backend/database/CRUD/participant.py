from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import Participant, ResearchSession, ParticipantCollection
from api.schemas import ParticipantCreate


class CRUDParticipant(CRUDBase[Participant, ParticipantCreate, None]):
    def create_for_session(self, db: Session, participant_in: ParticipantCreate,
                           db_session_r: ResearchSession) -> Participant:
        participant_in_data = jsonable_encoder(participant_in, by_alias=False)
        db_participant = Participant(**participant_in_data)
        db_participant.collection = ParticipantCollection()
        db_session_r.participant = db_participant
        return self._add_save(db, db_participant)
