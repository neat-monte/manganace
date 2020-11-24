from database.CRUD._crud_base import CRUDBase
from database.models import ResearchSession
from api.schemas import ResearchSessionCreate


class CRUDSessionR(CRUDBase[ResearchSession, ResearchSessionCreate, None]):
    pass
