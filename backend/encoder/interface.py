import random
import string
import uuid
from pathlib import Path
import matplotlib.pyplot as plt

from .wrapper import GeneratorWrapper


class GeneratorInterface:
    def __init__(self):
        self.generator = None

    def is_initialized(self) -> bool:
        return self.generator is not None

    def initialize(self) -> None:
        self.generator = GeneratorWrapper()
        # [Necessary] Dummy call to save internal variables
        _ = self.generator.generate_image_from_seed(0)

    def get_image_by_seed(self, seed: int, session: str) -> string:
        img = self.generator.generate_image_from_seed(seed)
        name = f'{seed}_{str(uuid.uuid4())}.png'
        path = Path.cwd() / 'static' / 'images' / 'sessions' / session / name
        plt.imsave(path, img)
        return name


generator = GeneratorInterface()
