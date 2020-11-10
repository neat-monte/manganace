from typing import List

from sqlalchemy.orm import Session

import crud
from schemas import Image, ImageUpdate, ImageCreate
from .image_file_service import ImageFileService


class ImageService:
    @staticmethod
    def get_image(db: Session, id_: int) -> Image:
        image = crud.image.get_with_tags(db, id_)
        if not image:
            return image
        return ImageService.construct_image(image)

    @staticmethod
    def get_images_of_collection(db: Session, collection_id: int) -> List[Image]:
        images = crud.image.get_images_of_with_tags(db, collection_id)
        result = []
        for image in images:
            result.append(ImageService.construct_image(image))
        return result

    @staticmethod
    def create_image(db: Session, image_in: ImageCreate):
        image = crud.image.create_with_tags(db, image_in)
        tags_ids = [tag.id for tag in image.tags]
        return ImageService.construct_image(image, tags_ids)

    @staticmethod
    def update_image(db: Session, id_: int, image_in: ImageUpdate):
        image = crud.image.get(db, id_)
        if not image:
            return image
        image = crud.image.update_with_tags(db, image, image_in)
        tags_ids = [tag.id for tag in image.tags]
        return ImageService.construct_image(image, tags_ids)

    @staticmethod
    def delete_image(db: Session, id_: int):
        image = crud.image.remove(db, id_)
        if not image:
            return image
        tags_ids = [tag.id for tag in image.tags]
        return ImageService.construct_image(image, tags_ids)

    @staticmethod
    def construct_image(image, tags_ids: [int] = None):
        if not tags_ids and hasattr(image, 'tags_ids') and image.tags_ids:
            tags_ids = list(map(int, image.tags_ids.split(",")))
        elif not tags_ids:
            tags_ids = []
        return Image.construct(
            id=image.id,
            seed=image.seed,
            filename=image.filename,
            url=ImageFileService.make_image_url(image.filename),
            description=image.description,
            collection_id=image.collection_id,
            tags_ids=tags_ids)
