from itertools import product
from typing import List

from sqlalchemy.orm import Session

import data
from models import Image
from schemas import TrialMeta, TrialImage
from .image_file_service import ImageFileService

image_file_service = ImageFileService()


class TrialService:
    def get_trials_meta(self, db: Session, session_r_id: int) -> List[TrialMeta]:
        vectors_ids = data.vector.get_ids(db)
        seeds = data.image.get_seeds_of_session(db, session_r_id)
        return [self.construct_trial_meta(s_id, v_id, seed)
                for (s_id, v_id, seed)
                in product([session_r_id], vectors_ids, seeds)]

    def get_trial_images(self, db: Session, meta: TrialMeta) -> List[TrialImage]:
        db_images = data.image.get_all_of_trial(db, meta.session_id, meta.seed, meta.vector_id)
        return [self.construct_trial_image(i, meta.vector_id) for i in db_images]

    @staticmethod
    def construct_trial_meta(session_id: int, vector_id: int, seed: int) -> TrialMeta:
        return TrialMeta.construct(session_id=session_id, vector_id=vector_id, seed=seed)

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
