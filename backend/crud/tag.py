from crud.base import CRUDBase
from models import Tag
from schemas import TagCreate, TagUpdate


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    pass
