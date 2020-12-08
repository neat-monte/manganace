from database.CRUD._crud_base import CRUDBase
from database.models import UserCollection
from api.schemas import CollectionCreate, CollectionUpdate


class CRUDUserCollection(CRUDBase[UserCollection, CollectionCreate, CollectionUpdate]):
    pass
