from typing import List

from sqlalchemy.orm import Session

from data._crud_base import CRUDBase
from models import Vector


# noinspection PyMethodMayBeStatic
class CRUDVector(CRUDBase[Vector, None, None]):
    def get_ids(self, db: Session) -> List[int]:
        return [i for (i,) in db.query(Vector.id).all()]
