from typing import List

from sqlalchemy.orm import Session

import crud
from schemas import Image, ImageUpdate, ImageCreate


class ImageService:
    def get_image(self, db: Session, id_: int) -> Image:
        image = crud.image.get_with_tags(db, id_)
        if not image:
            return image
        return self.construct_image(image)

    def get_images_of_collection(self, db: Session, collection_id: int) -> List[Image]:
        images = crud.image.get_images_of_with_tags(db, collection_id)
        result = []
        for image in images:
            result.append(self.construct_image(image))
        return result

    def create_image(self, db: Session, image_in: ImageCreate):
        image = crud.image.create_with_tags(db, image_in)
        tags_ids = [tag.id for tag in image.tags]
        return self.construct_image(image, tags_ids)

    def update_image(self, db: Session, id_: int, image_in: ImageUpdate):
        image = crud.image.get(db, id_)
        if not image:
            return image
        image = crud.image.update_with_tags(db, image, image_in)
        tags_ids = [tag.id for tag in image.tags]
        return self.construct_image(image, tags_ids)

    def delete_image(self, db: Session, id_: int):
        image = crud.image.remove(db, id_)
        if not image:
            return image
        tags_ids = [tag.id for tag in image.tags]
        return self.construct_image(image, tags_ids)

    @staticmethod
    def construct_image(image, tags_ids: [int] = None):
        if not tags_ids and hasattr(image, 'tags_ids') and image.tags_ids:
            tags_ids = list(map(int, image.tags_ids.split(",")))
        else:
            tags_ids = []
        return Image.construct(
            id=image.id,
            seed=image.seed,
            filename=image.filename,
            description=image.description,
            collection_id=image.collection_id,
            tags_ids=tags_ids)


image_service = ImageService()
