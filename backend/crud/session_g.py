from crud.base import CRUDBase
from models import GeneratorSession
from schemas import GeneratorSessionCreate, GeneratorSessionUpdate


class CRUDSessionG(CRUDBase[GeneratorSession, GeneratorSessionCreate, GeneratorSessionUpdate]):
    pass