from time import strftime
from pathlib import Path
from typing import List

import pandas as pd
from sqlalchemy.orm import Session

import data
import models as m
import schemas as s
from .vector_service import VectorService

vector_service = VectorService()


class ResearchService:
    ROOT = Path.cwd()
    EXPORTS = ROOT / 'static/exports'

    def get_results_data(self, db: Session) -> List[s.SingleVectorData]:
        effect_value_pairs = db.query(m.Vector.effect, m.ImageVector.multiplier) \
            .select_from(m.ParticipantCollection) \
            .join(m.CImage) \
            .join(m.Image) \
            .join(m.ImageVector) \
            .join(m.Vector) \
            .all()
        points_by_effect = {}
        for (effect, value) in effect_value_pairs:
            if effect not in points_by_effect:
                points_by_effect[effect] = []
            points_by_effect[effect].append(value)
        return [self.construct_vector_data(effect, points) for (effect, points) in points_by_effect.items()]

    def export_results_data(self, db: Session):
        participants = data.participant.get_all(db)
        results_data = {'age': [], 'gender': [], 'education': [], 'total_images': [], 'overlap': [],
                        'equalize_gender': [], 'slider_steps': [], 'emotion': [], 'multiplier': []}
        for participant in participants:
            for c_image in participant.collection.c_images:
                results_data['age'].append(participant.age)
                results_data['gender'].append(participant.gender.name)
                results_data['education'].append(participant.education.name)
                results_data['total_images'].append(participant.session.total_amount)
                results_data['overlap'].append(participant.session.overlap_amount)
                results_data['equalize_gender'].append(participant.session.equalize_gender)
                results_data['slider_steps'].append(participant.session.slider_steps)
                results_data['emotion'].append(c_image.image.vectors[0].vector.effect)
                results_data['multiplier'].append(c_image.image.vectors[0].multiplier)
        df = pd.DataFrame(results_data)
        file_path = self.EXPORTS / f'export_{strftime("%Y-%m-%d-%H-%M-%S")}.csv'
        df.to_csv(file_path)
        return str(file_path)

    def get_session_schema(self, db: Session, db_session_r: m.ResearchSession) -> s.ResearchSession:
        vectors_count = len(vector_service.get_ids(db))
        return self.construct_research_session(db_session_r, vectors_count)

    def get_sessions(self, db: Session) -> List[s.ResearchSession]:
        db_sessions_r = data.session_r.get_all(db)
        vectors_count = len(vector_service.get_ids(db))
        return [self.construct_research_session(ses, vectors_count) for ses in db_sessions_r]

    @staticmethod
    def construct_vector_data(effect: str, points: List[float]) -> s.SingleVectorData:
        return s.SingleVectorData.construct(
            effect=effect,
            points=points
        )

    @staticmethod
    def construct_research_session(db_session_r: m.ResearchSession, vectors_count: int) -> s.ResearchSession:
        trials = vectors_count * db_session_r.total_amount
        progress = 0
        if db_session_r.participant and db_session_r.participant.collection:
            progress = len(db_session_r.participant.collection.c_images)
        return s.ResearchSession.construct(
            id=db_session_r.id,
            total_amount=db_session_r.total_amount,
            overlap_amount=db_session_r.overlap_amount,
            equalize_gender=db_session_r.equalize_gender,
            slider_steps=db_session_r.slider_steps,
            created=db_session_r.created,
            trials=trials,
            progress=progress,
            participant=db_session_r.participant
        )
