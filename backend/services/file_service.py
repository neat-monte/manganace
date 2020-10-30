from pathlib import Path
from shutil import copy

from sqlalchemy.orm import Session

import crud


class ImageFileService:
    sessions = Path.cwd() / 'static' / 'images' / 'sessions'
    saved = Path.cwd() / 'static' / 'images' / 'saved'

    def image_exists(self, session: str, filename: str):
        image_loc = self.sessions / session / filename
        return image_loc.exists()

    def save_image(self, session: str, filename: str):
        image_loc = self.sessions / session / filename
        new_loc = self.saved / filename
        copy(image_loc, new_loc)

    def delete_image(self, db: Session, filename):
        image_loc = self.saved / filename
        if not crud.image.exists_with_filename(db, filename) and image_loc.exists():
            image_loc.unlink()


image_file_service = ImageFileService()
