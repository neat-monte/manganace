from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Image, Tag
from schemas import ImageCreate, ImageUpdate


# noinspection PyMethodMayBeStatic
class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create_with_tags(self, db: Session, image_in: ImageCreate) -> Image:
        tags = []
        if image_in.tags_ids:
            tags = db.query(Tag).filter(Tag.id.in_(image_in.tags_ids)).all()
        image_in_data = jsonable_encoder(image_in, exclude={"tags_ids"}, by_alias=False)
        db_image = Image(**image_in_data)
        db_image.tags = tags
        return self._add_save(db, db_image)

    def update_with_tags(self, db: Session, db_image: Image, image_in: ImageUpdate) -> Image:
        tags = db.query(Tag).filter(Tag.id.in_(image_in.tags_ids)).all()
        self._update_properties(db_image, image_in)
        return self._add_save(db, db_image)

    def get_images_of(self, db: Session, collection_id: int) -> List[Image]:
        return db.query(Image.id,
                        Image.seed,
                        Image.filename,
                        Image.description,
                        Image.collection_id,
                        func.group_concat(Tag.id).label('tags_ids')) \
            .filter_by(collection_id=collection_id) \
            .join(Image.tags) \
            .group_by(Image) \
            .all()


image = CRUDImage(Image)
