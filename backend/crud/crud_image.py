from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Image, Tag, Vector, ImageVector
from schemas import ImageCreate, ImageUpdate


# noinspection PyMethodMayBeStatic
class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def exists_with_filename(self, db: Session, filename: str):
        return db.query(Image.id).filter_by(filename=filename).first() is not None

    def get_all_of(self, db: Session, collection_id: int):
        return db.query(Image).filter(Image.collection_id == collection_id).all()

    def create_with_relations(self, db: Session, image_in: ImageCreate) -> Image:
        image_in_data = jsonable_encoder(image_in, exclude={"tags_ids", "vectors"}, by_alias=False)
        db_image = Image(**image_in_data)
        db_image.vectors = self._create_image_vectors(db, image_in)
        db_image.tags = self._get_image_tags(db, image_in)
        return self._add_save(db, db_image)

    def update_with_tags(self, db: Session, db_image: Image, image_in: ImageUpdate) -> Image:
        self._update_properties(db_image, image_in)
        db_image.tags = self._get_image_tags(db, image_in)
        return self._add_save(db, db_image)

    def delete_with_relations(self, db: Session, db_image: Image) -> Image:
        for image_vector in db_image.vectors:
            db.delete(image_vector)
        self._delete_save(db, db_image)
        return db_image

    def _create_image_vectors(self, db: Session, image_in: ImageCreate) -> List[ImageVector]:
        image_vectors = []
        if image_in.vectors:
            vectors_ids = [v.id for v in image_in.vectors]
            valid_vectors_ids = [i for i, in db.query(Vector.id).filter(Vector.id.in_(vectors_ids)).all()]
            for vector in [v for v in image_in.vectors if v.id in valid_vectors_ids]:
                image_vectors.append(ImageVector(vector_id=vector.id, multiplier=vector.multiplier))
        return image_vectors

    def _get_image_tags(self, db: Session, image_schema):
        image_tags = []
        if image_schema.tags_ids:
            image_tags = db.query(Tag).filter(Tag.id.in_(image_schema.tags_ids)).all()
        return image_tags


image = CRUDImage(Image)
