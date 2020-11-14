from typing import List, Optional

from sqlalchemy.orm import Session

import crud
import models as m
import schemas as s
from .image_file_service import image_file as image_file_service


class CImageService:
    def get_all_of_collection(self, db: Session, collection_id: int) -> List[s.CImage]:
        db_c_images = crud.c_image.get_all_of_collection(db, collection_id)
        return [self.construct_c_image(i) for i in db_c_images]

    def get(self, db: Session, id_: int) -> Optional[s.CImage]:
        db_c_image = crud.c_image.get(db, id_)
        if not db_c_image:
            return None
        return self.construct_c_image(db_c_image)

    def create(self, db: Session, c_image_in: s.CImageCreate) -> s.CImage:
        db_c_image = crud.c_image.create_with_tags(db, c_image_in)
        return self.construct_c_image(db_c_image)

    def update(self, db: Session, id_: int, c_image_in: s.CImageUpdate) -> Optional[s.CImage]:
        db_c_image = crud.c_image.get(db, id_)
        if not db_c_image:
            return None
        db_c_image = crud.c_image.update_with_tags(db, db_c_image, c_image_in)
        return self.construct_c_image(db_c_image)

    def delete(self, db: Session, id_: int) -> Optional[s.CImage]:
        db_c_image = crud.c_image.get(db, id_)
        if not db_c_image:
            return None
        db_c_image = crud.c_image.delete(db, db_c_image)
        return self.construct_c_image(db_c_image)

    @staticmethod
    def construct_c_image(db_c_image: m.CImage):
        return s.CImage.construct(
            id=db_c_image.id,
            collection_id=db_c_image.collection_id,
            image_id=db_c_image.image_id,
            session_id=db_c_image.image.session_id,
            seed=db_c_image.image.seed,
            description=db_c_image.description,
            tags_ids=[tag.id for tag in db_c_image.tags],
            url=image_file_service.make_url(db_c_image.image.filename, db_c_image.image.session_id),
            vectors=[s.ImageVector.construct(id=v.vector_id, multiplier=v.multiplier)
                     for v in db_c_image.image.vectors]
        )


c_image = CImageService()
