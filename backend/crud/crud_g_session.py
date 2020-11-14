from crud.base import CRUDBase
from models import GeneratorSession
from schemas import GeneratorSessionCreate, GeneratorSessionUpdate


class CRUDSession(CRUDBase[GeneratorSession, GeneratorSessionCreate, GeneratorSessionUpdate]):
    pass


g_session = CRUDSession(GeneratorSession)
