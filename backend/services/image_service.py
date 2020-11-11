from typing import List, Optional

from sqlalchemy.orm import Session

import crud
from schemas import Image, ImageUpdate, ImageCreate, VectorMultiplier
from .image_file_service import ImageFileService


class ImageService:
    @staticmethod
    def get_image(db: Session, id_: int) -> Optional[Image]:
        db_image = crud.image.get(db, id_)
        if not db_image:
            return None
        return ImageService.construct_image(db_image)

    @staticmethod
    def get_images_of_collection(db: Session, collection_id: int) -> List[Image]:
        db_images = crud.image.get_all_of(db, collection_id)
        return [ImageService.construct_image(db_image) for db_image in db_images]

    @staticmethod
    def create_image(db: Session, image_in: ImageCreate) -> Optional[Image]:
        db_image = crud.image.create_with_relations(db, image_in)
        return ImageService.construct_image(db_image)

    @staticmethod
    def update_image(db: Session, id_: int, image_in: ImageUpdate) -> Optional[Image]:
        db_image = crud.image.get(db, id_)
        if not db_image:
            return None
        db_image = crud.image.update_with_tags(db, db_image, image_in)
        return ImageService.construct_image(db_image)

    @staticmethod
    def delete_image(db: Session, id_: int) -> Optional[Image]:
        db_image = crud.image.get(db, id_)
        if not db_image:
            return None
        _ = crud.image.delete_with_relations(db, db_image)
        return ImageService.construct_image(db_image)

    @staticmethod
    def construct_image(image):
        return Image.construct(
            id=image.id,
            seed=image.seed,
            filename=image.filename,
            description=image.description,
            collection_id=image.collection_id,
            vectors=[VectorMultiplier.construct(id=v.vector_id, multiplier=v.multiplier) for v in image.vectors],
            tags_ids=[tag.id for tag in image.tags],
            url=ImageFileService.make_image_url(image.filename)
        )
