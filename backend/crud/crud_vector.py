from crud.base import CRUDBase
from models import Vector


class CRUDVector(CRUDBase[Vector, None, None]):
    pass


vector = CRUDVector(Vector)
