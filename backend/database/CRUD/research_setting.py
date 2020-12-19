from database.CRUD._crud_base import CRUDBase
from database.models import ResearchSetting
from api.schemas import ResearchSettingCreate


class CRUDResearchSetting(CRUDBase[ResearchSetting, ResearchSettingCreate, None]):
    pass
