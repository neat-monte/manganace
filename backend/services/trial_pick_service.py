from typing import List, Optional

from sqlalchemy.orm import Session

from database import models as m, CRUD
from api import schemas as s
from .image_file_service import ImageFileService

image_file_service = ImageFileService()


class TrialPickService:
    def get_all_of_collection(self, db: Session, collection_id: int) -> List[s.TrialPick]:
        db_trial_picks = CRUD.trial_pick.get_all_of_collection(db, collection_id)
        return [self.construct_trial_pick(i) for i in db_trial_picks]

    def get(self, db: Session, id_: int) -> Optional[s.TrialPick]:
        db_trial_pick = CRUD.trial_pick.get(db, id_)
        if not db_trial_pick:
            return None
        return self.construct_trial_pick(db_trial_pick)

    def create(self, db: Session, trial_pick_in: s.TrialPickCreate) -> s.TrialPick:
        db_trial_pick = CRUD.trial_pick.create_with_tags(db, trial_pick_in)
        return self.construct_trial_pick(db_trial_pick)

    @staticmethod
    def construct_trial_pick(db_trial_pick: m.TrialPick):
        return s.TrialPick.construct(
            id=db_trial_pick.id,
            collection_id=db_trial_pick.collection_id,
            image_id=db_trial_pick.image_id,
            session_id=db_trial_pick.image.session_id,
            seed=db_trial_pick.image.seed,
            description=db_trial_pick.description,
            tags_ids=[tag.id for tag in db_trial_pick.tags],
            url=image_file_service.make_url(db_trial_pick.image.filename, db_trial_pick.image.session_id),
            vectors=[s.ImageVector.construct(id=v.vector_id, multiplier=v.multiplier)
                     for v in db_trial_pick.image.vectors],
            trial_number=db_trial_pick.trial_number,
            initial_multiplier=db_trial_pick.initial_multiplier,
            created=db_trial_pick.created
        )
