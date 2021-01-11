from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import Participant, ResearchSession, ParticipantCollection
from api.schemas import ParticipantCreate


# noinspection PyMethodMayBeStatic
class CRUDParticipant(CRUDBase[Participant, ParticipantCreate, None]):
    def create_for_session(self, db: Session, participant_in: ParticipantCreate,
                           db_research_session: ResearchSession) -> Participant:
        participant_in_data = jsonable_encoder(participant_in, exclude={"consented_on"}, by_alias=False)
        participant_in_data["consented_on"] = str(participant_in.consented_on)
        db_participant = Participant(**participant_in_data)
        db_participant.consented_on = participant_in.consented_on
        db_participant.collection = ParticipantCollection()
        db_research_session.participant = db_participant
        return self._add_save(db, db_participant)

    def get_all_of_research_setting(self, db: Session, research_setting_id):
        return db.query(Participant) \
            .join(ResearchSession) \
            .filter(ResearchSession.research_setting_id == research_setting_id) \
            .all()
