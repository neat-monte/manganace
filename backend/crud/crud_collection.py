from crud.base import CRUDBase
from models import Collection
from schemas import CollectionCreate, CollectionUpdate


class CRUDCollection(CRUDBase[Collection, CollectionCreate, CollectionUpdate]):
    pass


collection = CRUDCollection(Collection)
