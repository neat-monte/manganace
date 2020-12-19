from typing import List, Optional

from sqlalchemy.orm import Session

from database import models as m, CRUD
from api import schemas as s
from .image_file_service import ImageFileService

image_file_service = ImageFileService()


class CImageService:
    def get_all_of_collection(self, db: Session, collection_id: int) -> List[s.CImage]:
        db_collection_images = CRUD.collection_image.get_all_of_collection(db, collection_id)
        return [self.construct_collection_image(i) for i in db_collection_images]

    def get(self, db: Session, id_: int) -> Optional[s.CImage]:
        db_collection_image = CRUD.collection_image.get(db, id_)
        if not db_collection_image:
            return None
        return self.construct_collection_image(db_collection_image)

    def create(self, db: Session, collection_image_in: s.CImageCreate) -> s.CImage:
        db_collection_image = CRUD.collection_image.create_with_tags(db, collection_image_in)
        return self.construct_collection_image(db_collection_image)

    def update(self, db: Session, id_: int, collection_image_in: s.CImageUpdate) -> Optional[s.CImage]:
        db_collection_image = CRUD.collection_image.get(db, id_)
        if not db_collection_image:
            return None
        db_collection_image = CRUD.collection_image.update_with_tags(db, db_collection_image, collection_image_in)
        return self.construct_collection_image(db_collection_image)

    def delete(self, db: Session, id_: int) -> Optional[s.CImage]:
        db_collection_image = CRUD.collection_image.get(db, id_)
        if not db_collection_image:
            return None
        deleted = self.construct_collection_image(db_collection_image)
        _ = CRUD.collection_image.delete(db, id_)
        return deleted

    @staticmethod
    def construct_collection_image(db_collection_image: m.CImage):
        return s.CImage.construct(
            id=db_collection_image.id,
            collection_id=db_collection_image.collection_id,
            image_id=db_collection_image.image_id,
            session_id=db_collection_image.image.session_id,
            seed=db_collection_image.image.seed,
            description=db_collection_image.description,
            tags_ids=[tag.id for tag in db_collection_image.tags],
            url=image_file_service.make_url(db_collection_image.image.filename, db_collection_image.image.session_id),
            vectors=[s.ImageVector.construct(id=v.vector_id, multiplier=v.multiplier)
                     for v in db_collection_image.image.vectors]
        )
