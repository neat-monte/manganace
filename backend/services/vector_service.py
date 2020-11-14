from sqlalchemy.orm import Session

import crud
from schemas import Vector


class VectorService:
    @staticmethod
    def get_vectors(db: Session):
        db_vectors = crud.vector.get_all(db)
        return [Vector.construct(id=v.id, name=v.name, effect=v.effect, weight=v.weight) for v in db_vectors]

    @staticmethod
    def get_vectors_dict(db: Session):
        db_vectors = crud.vector.get_all(db)
        return {v.id: (v.effect, v.weight) for v in db_vectors}


vector = VectorService()
