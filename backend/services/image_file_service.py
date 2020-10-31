from urllib import parse
from pathlib import Path
from shutil import copy

from sqlalchemy.orm import Session

import crud
from config import settings


class ImageFileService:
    RELATIVE_SESSIONS_PATH = 'static/images/sessions'
    RELATIVE_SAVED_PATH = 'static/images/saved'
    SESSIONS_PATH = Path.cwd() / RELATIVE_SESSIONS_PATH
    SAVED_PATH = Path.cwd() / RELATIVE_SAVED_PATH

    @staticmethod
    def make_image_url(filename: str, session: str = None):
        url = parse.urlunsplit(('http', f'{settings.BACKEND_HOST_DOMAIN}:{settings.BACKEND_HOST_PORT}', '', '', ''))
        return parse.urljoin(url, f'{ImageFileService.RELATIVE_SAVED_PATH}/{filename}') if not session \
            else parse.urljoin(url, f'{ImageFileService.RELATIVE_SESSIONS_PATH}/{session}/{filename}')

    @staticmethod
    def image_exists(session: str, filename: str):
        image_loc = ImageFileService.SESSIONS_PATH / session / filename
        return image_loc.exists()

    @staticmethod
    def save_image(session: str, filename: str):
        image_loc = ImageFileService.SESSIONS_PATH / session / filename
        new_loc = ImageFileService.SAVED_PATH / filename
        copy(image_loc, new_loc)

    @staticmethod
    def delete_image(db: Session, filename):
        image_loc = ImageFileService.SAVED_PATH / filename
        if not crud.image.exists_with_filename(db, filename) and image_loc.exists():
            image_loc.unlink()
