from typing import List, Optional

from sqlalchemy.orm import Session

import data
import models as m
import schemas as s
from .image_file_service import ImageFileService

image_file_service = ImageFileService()


class ImageService:
    def get_all_of_session(self, db: Session, session_id: int) -> List[s.Image]:
        db_images = data.image.get_all_of_session(db, session_id)
        return [self.construct_image(i) for i in db_images]

    def get(self, db: Session, id_: int) -> Optional[s.Image]:
        db_image = data.image.get(db, id_)
        if not db_image:
            return None
        return self.construct_image(db_image)

    def create(self, db: Session, request: s.GenerateRequest, filename: str) -> s.Image:
        db_image = data.image.create_with_vectors(db, request.seed, filename, request.session_id, request.vectors)
        return self.construct_image(db_image)

    @staticmethod
    def construct_image(db_image: m.Image) -> s.Image:
        return s.Image.construct(
            id=db_image.id,
            seed=db_image.seed,
            session_id=db_image.session_id,
            url=image_file_service.make_url(db_image.filename, db_image.session_id),
            vectors=[s.ImageVector.construct(id=v.vector_id, multiplier=v.multiplier)
                     for v in db_image.vectors]
        )
