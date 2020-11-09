import string
import uuid
from pathlib import Path

import matplotlib.pyplot as plt
from sqlalchemy.orm import Session

from encoder.wrapper import GeneratorWrapper
from schemas import GenerateRequest
from .emotion_service import EmotionService


# noinspection PyMethodMayBeStatic
class GeneratorService:
    generator = None

    def initialize(self, db: Session) -> None:
        emotions_name_weight_by_id = EmotionService.get_emotions_dict(db)
        self.generator = GeneratorWrapper(emotions_name_weight_by_id)
        _ = self.generator.generate(0)  # [Necessary] Dummy call to save internal variables

    def is_initialized(self) -> bool:
        return self.generator is not None

    def generate_image(self, request: GenerateRequest, session: str) -> string:
        img = self.generator.generate(request.seed, request.emotions)
        return self._save_image(img, request.seed, session)

    def _save_image(self, img, seed: int, session: str):
        name = f'{seed}_{str(uuid.uuid4())}.png'
        path = Path.cwd() / 'static' / 'images' / 'sessions' / session / name
        plt.imsave(path, img)
        return name


GeneratorService = GeneratorService()
