from sqlalchemy.orm import Session

import crud
from schemas import Vector


class VectorService:
    @staticmethod
    def get_vectors(db: Session):
        vs = crud.vector.get_all(db)
        vectors = []
        for v in vs:
            vector = Vector.construct(id=v.id, name=v.name, effect=v.effect, weight=v.weight)
            vectors.append(vector)
        return vectors

    @staticmethod
    def get_vectors_dict(db: Session):
        vs = crud.vector.get_all(db)
        effect_weight_by_id = {}
        for v in vs:
            effect_weight_by_id[v.id] = (v.effect, v.weight)
        return effect_weight_by_id
