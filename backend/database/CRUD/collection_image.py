from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.CRUD._crud_base import CRUDBase
from database.models import CollectionImage, Tag
from api.schemas import CollectionImageCreate, CollectionImageUpdate


# noinspection PyMethodMayBeStatic
class CRUDCollectionImage(CRUDBase[CollectionImage, CollectionImageCreate, CollectionImageUpdate]):
    def get_all_of_collection(self, db: Session, collection_id: int):
        return db.query(CollectionImage).filter(CollectionImage.collection_id == collection_id).all()

    def create_with_tags(self, db: Session, collection_image_in: CollectionImageCreate) -> CollectionImage:
        collection_image_in_data = jsonable_encoder(collection_image_in, exclude={"tags_ids"}, by_alias=False)
        db_collection_image = CollectionImage(**collection_image_in_data)
        db_collection_image.tags = self._get_image_tags(db, collection_image_in)
        return self._add_save(db, db_collection_image)

    def update_with_tags(self, db: Session, db_collection_image: CollectionImage, image_in: CollectionImageUpdate) -> CollectionImage:
        self._update_properties(db_collection_image, image_in)
        db_collection_image.tags = self._get_image_tags(db, image_in)
        return self._add_save(db, db_collection_image)

    def _get_image_tags(self, db: Session, collection_image_schema):
        if collection_image_schema.tags_ids:
            return db.query(Tag).filter(Tag.id.in_(collection_image_schema.tags_ids)).all()
        return []
