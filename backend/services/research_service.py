from sqlalchemy.orm import Session

import crud
import models as m
import schemas as s
from .vector_service import VectorService

vector_service = VectorService()


class ResearchService:
    def get_session_schema(self, db: Session, db_session_r: m.ResearchSession) -> s.ResearchSession:
        vectors_count = len(vector_service.get_ids(db))
        return self.construct_research_session(db_session_r, vectors_count)

    def get_sessions(self, db: Session):
        db_sessions_r = crud.session_r.get_all(db)
        vectors_count = len(vector_service.get_ids(db))
        return [self.construct_research_session(ses, vectors_count) for ses in db_sessions_r]

    @staticmethod
    def construct_research_session(db_session_r: m.ResearchSession, vectors_count: int) -> s.ResearchSession:
        trials = vectors_count * db_session_r.total_amount
        progress = 0
        if db_session_r.participant and db_session_r.participant.collection:
            progress = len(db_session_r.participant.collection.images)
        return s.ResearchSession.construct(
            id=db_session_r.id,
            total_amount=db_session_r.total_amount,
            overlap_amount=db_session_r.overlap_amount,
            equalize_gender=db_session_r.equalize_gender,
            slider_steps=db_session_r.slider_steps,
            created=db_session_r.created,
            trials=trials,
            progress=progress
        )
