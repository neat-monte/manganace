from typing import List

from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import Tag
from api.schemas import TagCreate, TagUpdate


# noinspection PyMethodMayBeStatic
class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def get_all_research(self, db: Session) -> List[Tag]:
        return db.query(Tag).filter(Tag.for_research).all()
