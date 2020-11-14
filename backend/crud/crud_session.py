from crud.base import CRUDBase
from models import Session
from schemas import GeneratorSessionCreate, GeneratorSessionUpdate


class CRUDSession(CRUDBase[Session, GeneratorSessionCreate, GeneratorSessionUpdate]):
    pass


session = CRUDSession(Session)
