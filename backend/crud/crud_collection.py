from sqlalchemy.orm import Session, load_only

from crud.base import CRUDBase
from models import Collection, Image
from schemas import CollectionCreate, CollectionUpdate


class CRUDCollection(CRUDBase[Collection, CollectionCreate, CollectionUpdate]):
    pass


collection = CRUDCollection(Collection)
