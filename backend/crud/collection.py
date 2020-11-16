from crud.base import CRUDBase
from models import UserCollection
from schemas import CollectionCreate, CollectionUpdate


class CRUDUserCollection(CRUDBase[UserCollection, CollectionCreate, CollectionUpdate]):
    pass
