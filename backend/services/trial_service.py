from itertools import product
from typing import List

from sqlalchemy.orm import Session

import data
from models import Image, ResearchSession
from schemas import TrialMeta, TrialImage
from .image_file_service import ImageFileService

image_file_service = ImageFileService()


class TrialService:
    def get_trials_meta(self, db: Session, db_session_r: ResearchSession,
                        include_done: bool = False) -> List[TrialMeta]:
        vectors = data.vector.get_all(db)
        seeds = data.image.get_seeds_of_session(db, db_session_r.id)
        if include_done:
            return [self.construct_trial_meta(s_id, v.id, seed, v.effect)
                    for (s_id, v, seed)
                    in product([db_session_r.id], vectors, seeds)]
        done_trial = [(c_im.image.vectors[0].vector_id, c_im.image.seed)
                      for c_im in db_session_r.participant.collection.c_images]
        return [self.construct_trial_meta(s_id, v.id, seed, v.effect)
                for (s_id, v, seed)
                in product([db_session_r.id], vectors, seeds)
                if (v.id, seed) not in done_trial]

    def get_trial_images(self, db: Session, meta: TrialMeta) -> List[TrialImage]:
        db_images = data.image.get_all_of_trial(db, meta.session_id, meta.seed, meta.vector_id)
        images = [self.construct_trial_image(i, meta.vector_id) for i in db_images]
        images.sort(key=lambda i: i.vector_multiplier)
        return images

    @staticmethod
    def construct_trial_meta(session_id: int, vector_id: int, seed: int, emotion: str) -> TrialMeta:
        return TrialMeta.construct(session_id=session_id, vector_id=vector_id, seed=seed, emotion=emotion)

    @staticmethod
    def construct_trial_image(image: Image, vector_id: int) -> TrialImage:
        vector = next(filter(lambda v: v.vector_id == vector_id, image.vectors), None)
        if not vector:
            raise ValueError("Vector not found...")
        return TrialImage.construct(
            id=image.id,
            url=image_file_service.make_url(image.filename, image.session_id),
            vector_multiplier=vector.multiplier
        )
