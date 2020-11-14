from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import CImage, Tag
from schemas import CImageCreate, CImageUpdate


# noinspection PyMethodMayBeStatic
class CRUDCImage(CRUDBase[CImage, CImageCreate, CImageUpdate]):
    def get_all_of_collection(self, db: Session, collection_id: int):
        return db.query(CImage).filter(CImage.collection_id == collection_id).all()

    def create_with_tags(self, db: Session, c_image_in: CImageCreate) -> CImage:
        c_image_in_data = jsonable_encoder(c_image_in, exclude={"tags_ids"}, by_alias=False)
        db_c_image = CImage(**c_image_in_data)
        db_c_image.tags = self._get_image_tags(db, c_image_in)
        return self._add_save(db, db_c_image)

    def update_with_tags(self, db: Session, db_c_image: CImage, image_in: CImageUpdate) -> CImage:
        self._update_properties(db_c_image, image_in)
        db_c_image.tags = self._get_image_tags(db, image_in)
        return self._add_save(db, db_c_image)

    def _get_image_tags(self, db: Session, c_image_schema):
        if c_image_schema.tags_ids:
            return db.query(Tag).filter(Tag.id.in_(c_image_schema.tags_ids)).all()
        return []


c_image = CRUDCImage(CImage)
