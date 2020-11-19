from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

import data
from schemas import Vector


# noinspection PyMethodMayBeStatic
class VectorService:
    def get_ids(self, db: Session) -> List[int]:
        return data.vector.get_ids(db)

    def get(self, db: Session) -> List[Vector]:
        db_vectors = data.vector.get_all(db)
        return [Vector.construct(id=v.id, name=v.name, effect=v.effect, weight=v.weight) for v in db_vectors]

    def get_dict(self, db: Session) -> Dict[int, Tuple[str, float]]:
        db_vectors = data.vector.get_all(db)
        return {v.id: (v.effect, v.weight) for v in db_vectors}
