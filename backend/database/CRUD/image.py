from typing import List

from sqlalchemy.orm import Session, joinedload

from api import schemas as s
from database.CRUD._crud_base import CRUDBase
from database.models import Image, Vector, ImageVector


# noinspection PyMethodMayBeStatic
class CRUDImage(CRUDBase[Image, None, None]):
    def get_all_of_session(self, db: Session, session_id: int) -> List[Image]:
        return db.query(Image).filter(Image.session_id == session_id).all()

    def get_seeds_of_session(self, db: Session, session_id: int) -> List[int]:
        return [seed for (seed,) in db.query(Image.seed).filter(Image.session_id == session_id).distinct().all()]

    def get_all_of_trial(self, db: Session, session_id: int, seed: int, vector_id: int) -> List[Image]:
        return db.query(Image).filter(
            Image.session_id == session_id,
            Image.seed == seed,
            ImageVector.vector_id == vector_id
        ).join(ImageVector).options(joinedload('vectors')).all()

    def create_with_vectors(self, db: Session, seed: int, filename: str,
                            session_id: int, vectors: List[s.ImageVector]) -> Image:
        db_image = Image(seed=seed, filename=filename, session_id=session_id)
        db_image.vectors = self._create_image_vectors(db, vectors)
        return self._add_save(db, db_image)

    def delete_with_vectors(self, db: Session, db_image: Image) -> Image:
        for image_vector in db_image.vectors:
            db.delete(image_vector)
        self._delete_save(db, db_image)
        return db_image

    def _create_image_vectors(self, db: Session, vectors: List[s.ImageVector]) -> List[ImageVector]:
        image_vectors = []
        vectors_ids = [v.id for v in vectors]
        valid_vectors_ids = [i for i, in db.query(Vector.id).filter(Vector.id.in_(vectors_ids)).all()]
        for vector in [v for v in vectors if v.id in valid_vectors_ids]:
            image_vectors.append(ImageVector(vector_id=vector.id, multiplier=vector.multiplier))
        return image_vectors
