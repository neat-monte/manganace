from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import TrialPick, Tag
from api.schemas import TrialPickCreate


# noinspection PyMethodMayBeStatic
class CRUDTrialPick(CRUDBase[TrialPick, TrialPickCreate, None]):
    def get_all_of_collection(self, db: Session, collection_id: int):
        return db.query(TrialPick).filter(TrialPick.collection_id == collection_id).all()

    def create_with_tags(self, db: Session, trial_pick_in: TrialPickCreate) -> TrialPick:
        trial_pick_in_data = jsonable_encoder(trial_pick_in, exclude={"tags_ids"}, by_alias=False)
        db_trial_pick = TrialPick(**trial_pick_in_data)
        db_trial_pick.tags = self._get_image_tags(db, trial_pick_in)
        return self._add_save(db, db_trial_pick)

    def _get_image_tags(self, db: Session, trial_pick_schema):
        if trial_pick_schema.tags_ids:
            return db.query(Tag).filter(Tag.id.in_(trial_pick_schema.tags_ids)).all()
        return []
