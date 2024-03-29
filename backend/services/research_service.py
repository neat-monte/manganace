from itertools import product
from pathlib import Path
from time import strftime
from typing import List

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from database import models as m, CRUD
from api import schemas as s
from .image_file_service import ImageFileService
from .vector_service import VectorService

image_file_service = ImageFileService()
vector_service = VectorService()


class ResearchService:
    ROOT = Path.cwd()
    EXPORTS = ROOT / 'static/exports'

    EXPORTS.mkdir(parents=True, exist_ok=True)

    def get_results_data(self, db: Session, research_setting_id: int, research_session_id: int = None) \
            -> List[s.SingleVectorData]:
        query = db.query(m.Vector.effect, m.ImageVector.multiplier).select_from(m.ResearchSession) \
            .filter(m.ResearchSession.research_setting_id == research_setting_id)
        if research_session_id:
            query = query.filter(m.ResearchSession.id == research_session_id) \
                .join(m.Participant).join(m.ParticipantCollection)
        else:
            query = query.join(m.Participant).join(m.ParticipantCollection)
        query = query.join(m.CollectionImage).join(m.Image).join(m.ImageVector).join(m.Vector)

        effect_value_pairs = query.all()
        points_by_effect = {}

        for (effect, value) in effect_value_pairs:
            if effect not in points_by_effect:
                points_by_effect[effect] = []
            points_by_effect[effect].append(value)

        data_by_effect = [self.construct_vector_data(effect, points) for (effect, points) in points_by_effect.items()]
        return sorted(data_by_effect, key=lambda x: x.effect)

    def export_results_data(self, db: Session, research_setting_id: int):
        setting = CRUD.research_setting.get(db, research_setting_id)
        participants = CRUD.participant.get_all_of_research_setting(db, research_setting_id)
        results_data = {'name': setting.name, 'total_images': setting.total_amount, 'overlap': setting.overlap_amount,
                        'equalize_gender': setting.equalize_gender, 'slider_steps': setting.slider_steps,
                        'global_multiplier': setting.global_multiplier, 'participants': []}
        for participant in participants:
            participant_data = {'age': participant.age, 'gender': participant.gender.name,
                                'start_time': participant.collection.created.strftime("%Y-%m-%d, %H:%M:%S"),
                                'trials': []}
            for trial_pick in participant.collection.trial_picks:
                participant_data['trials'].append(
                    {'trial_number': trial_pick.trial_number,
                     'emotion': trial_pick.image.vectors[0].vector.effect,
                     'initial_multiplier': trial_pick.initial_multiplier,
                     'chosen_multiplier': trial_pick.image.vectors[0].multiplier,
                     'choice_time': trial_pick.created.strftime("%Y-%m-%d, %H:%M:%S")})
            results_data['participants'].append(participant_data)
        df = pd.DataFrame(results_data)
        file_path = self.EXPORTS / f'export_{strftime("%Y-%m-%d-%H-%M-%S")}.csv'
        df.to_csv(file_path)
        return str(file_path)

    def get_session_schema(self, db: Session, db_research_session: m.ResearchSession) -> s.ResearchSession:
        vectors_count = len(vector_service.get_ids(db))
        return self.construct_research_session(db_research_session, vectors_count)

    def get_sessions(self, db: Session, research_setting_id: int) -> List[s.ResearchSession]:
        db_research_sessions = CRUD.research_session.get_all_of_setting(db, research_setting_id)
        vectors_count = len(vector_service.get_ids(db))
        return [self.construct_research_session(ses, vectors_count) for ses in db_research_sessions]

    def get_trials_meta(self, db: Session, db_research_session: m.ResearchSession,
                        include_done: bool = False) -> List[s.TrialMeta]:
        vectors = CRUD.vector.get_all(db)
        seeds = CRUD.image.get_seeds_of_session(db, db_research_session.id)
        if include_done:
            return [self.construct_trial_meta(s_id, v.id, seed, v.effect)
                    for (s_id, v, seed)
                    in product([db_research_session.id], vectors, seeds)]
        done_trial = [(collection_im.image.vectors[0].vector_id, collection_im.image.seed)
                      for collection_im in db_research_session.participant.collection.trial_picks]
        return [self.construct_trial_meta(s_id, v.id, seed, v.effect)
                for (s_id, v, seed)
                in product([db_research_session.id], vectors, seeds)
                if (v.id, seed) not in done_trial]

    def get_trial_images(self, db: Session, meta: s.TrialMeta) -> List[s.TrialImage]:
        db_images = CRUD.image.get_all_of_trial(db, meta.session_id, meta.seed, meta.vector_id)
        images = [self.construct_trial_image(i, meta.vector_id) for i in db_images]
        images.sort(key=lambda i: i.vector_multiplier)
        return images

    @staticmethod
    def construct_vector_data(effect: str, points: List[float]) -> s.SingleVectorData:
        return s.SingleVectorData.construct(
            effect=effect,
            points=points
        )

    @staticmethod
    def construct_research_session(db_research_session: m.ResearchSession, vectors_count: int) -> s.ResearchSession:
        trials = vectors_count * db_research_session.research_setting.total_amount
        progress = 0
        if db_research_session.participant and db_research_session.participant.collection:
            progress = len(db_research_session.participant.collection.trial_picks)
        return s.ResearchSession.construct(
            id=db_research_session.id,
            research_setting_id=db_research_session.research_setting_id,
            created=db_research_session.created,
            trials=trials,
            progress=progress,
            participant=db_research_session.participant
        )

    @staticmethod
    def construct_trial_meta(session_id: int, vector_id: int, seed: int, emotion: str) -> s.TrialMeta:
        return s.TrialMeta.construct(session_id=session_id, vector_id=vector_id, seed=seed, emotion=emotion)

    @staticmethod
    def construct_trial_image(image: m.Image, vector_id: int) -> s.TrialImage:
        vector = next(filter(lambda v: v.vector_id == vector_id, image.vectors), None)
        if not vector:
            raise ValueError("Vector not found...")
        return s.TrialImage.construct(
            id=image.id,
            url=image_file_service.make_url(image.filename, image.session_id),
            vector_multiplier=vector.multiplier
        )
