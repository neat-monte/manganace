import uuid
from pathlib import Path
from urllib import parse

import matplotlib.pyplot as plt

from config import settings


class ImageFileService:
    ROOT = Path.cwd()
    SESSIONS = ROOT / 'static' / 'images' / 'sessions'

    def make_url(self, filename: str, session_id: int):
        url = parse.urlunsplit(('http', f'{settings.BACKEND_HOST_DOMAIN}:{settings.BACKEND_HOST_PORT}', '', '', ''))
        return parse.urljoin(url, f'{self.SESSIONS}/{session_id}/{filename}')

    def save_generated_image(self, rgb_3d_array, seed: int, session_id: int):
        session_dir = self.SESSIONS / str(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        filename = f'{seed}_{str(uuid.uuid4())}.png'
        filepath = session_dir / filename
        plt.imsave(filepath, rgb_3d_array)
        return filename

    # RELATIVE_SESSIONS_PATH = 'static/images/sessions'
    # RELATIVE_SAVED_PATH = 'static/images/saved'
    # SESSIONS_PATH = Path.cwd() / RELATIVE_SESSIONS_PATH
    # SAVED_PATH = Path.cwd() / RELATIVE_SAVED_PATH
    #
    # @staticmethod
    # def make_image_url(filename: str, session: str = None):
    #     url = parse.urlunsplit(('http', f'{settings.BACKEND_HOST_DOMAIN}:{settings.BACKEND_HOST_PORT}', '', '', ''))
    #     return parse.urljoin(url, f'{ImageFileService.RELATIVE_SAVED_PATH}/{filename}') if not session \
    #         else parse.urljoin(url, f'{ImageFileService.RELATIVE_SESSIONS_PATH}/{session}/{filename}')
    #
    # @staticmethod
    # def image_exists(session: str, filename: str):
    #     image_loc = ImageFileService.SESSIONS_PATH / session / filename
    #     return image_loc.exists()
    #
    # @staticmethod
    # def save_image(session: str, filename: str):
    #     image_loc = ImageFileService.SESSIONS_PATH / session / filename
    #     new_loc = ImageFileService.SAVED_PATH / filename
    #     copy(image_loc, new_loc)
    #
    # @staticmethod
    # def delete_image(db: Session, filename):
    #     image_loc = ImageFileService.SAVED_PATH / filename
    #     if not crud.image.exists_with_filename(db, filename) and image_loc.exists():
    #         image_loc.unlink()


image_file = ImageFileService()
