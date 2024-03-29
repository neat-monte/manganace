import uuid
from pathlib import Path
from urllib import parse

import matplotlib.pyplot as plt

from config import settings


class ImageFileService:
    ROOT = Path.cwd()
    SESSION_IMAGES = 'static/session_images'

    def get_folder_path(self, session_id):
        return self.ROOT / self.SESSION_IMAGES / str(session_id)

    def get_path(self, filename: str, session_id: int) -> Path:
        return self.ROOT / self.SESSION_IMAGES / str(session_id) / filename

    def make_url(self, filename: str, session_id: int):
        url = parse.urlunsplit(('http', f'{settings.BACKEND_HOST_DOMAIN}:{settings.BACKEND_HOST_PORT}', '', '', ''))
        return parse.urljoin(url, f'{str(self.SESSION_IMAGES)}/{session_id}/{filename}')

    def save_generated_image(self, rgb_3d_array, seed: int, session_id: int) -> str:
        session_dir = self.ROOT / self.SESSION_IMAGES / str(session_id)
        session_dir.mkdir(parents=True, exist_ok=True)
        filename = f'{seed}_{str(uuid.uuid4())}.png'
        filepath = session_dir / filename
        plt.imsave(filepath, rgb_3d_array)
        return filename
