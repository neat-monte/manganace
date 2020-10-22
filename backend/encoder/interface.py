import random
import string

import matplotlib.pyplot as plt

from . import *
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

    def get_image_by_seed(self, seed: int) -> string:
        img = self.generator.generate_image_from_seed(seed)
        name = f'{seed}_{"".join(random.choice(string.ascii_letters) for _ in range(8))}.png'
        path = f'{STATIC}{name}'
        plt.imsave(path, img)
        return path


generator = GeneratorInterface()
