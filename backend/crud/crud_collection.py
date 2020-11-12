from crud.base import CRUDBase
from models import Collection
from schemas import CollectionCreate, CollectionUpdate


class CRUDUserCollection(CRUDBase[Collection, CollectionCreate, CollectionUpdate]):
    pass


collection = CRUDUserCollection(Collection)
