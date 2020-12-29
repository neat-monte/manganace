from typing import List

from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import ResearchSession
from api.schemas import ResearchSessionCreate


# noinspection PyMethodMayBeStatic
class CRUDResearchSession(CRUDBase[ResearchSession, ResearchSessionCreate, None]):
    def get_all_of_setting(self, db: Session, research_setting_id: int) -> List[ResearchSession]:
        return db.query(ResearchSession).filter(ResearchSession.research_setting_id == research_setting_id).all()
