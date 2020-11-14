from crud.base import CRUDBase
from models import Session


class CRUDSession(CRUDBase[Session, None, None]):
    pass


session = CRUDSession(Session)
