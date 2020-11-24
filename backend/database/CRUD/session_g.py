from database.CRUD._crud_base import CRUDBase
from database.models import GeneratorSession
from api.schemas import GeneratorSessionCreate, GeneratorSessionUpdate


class CRUDSessionG(CRUDBase[GeneratorSession, GeneratorSessionCreate, GeneratorSessionUpdate]):
    pass
