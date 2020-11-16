from crud.base import CRUDBase
from models import ResearchSession
from schemas import ResearchSessionCreate


class CRUDSessionR(CRUDBase[ResearchSession, ResearchSessionCreate, None]):
    pass
