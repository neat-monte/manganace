import math
import multiprocessing
from itertools import product, cycle
from typing import List

import numpy as np
from joblib import Parallel, delayed
from sqlalchemy.orm import Session

import database.models as m
from api.schemas import GenerateRequest, Image
from database.models import ResearchSession
from encoder.wrapper import GeneratorWrapper
from .image_file_service import ImageFileService
from .image_service import ImageService
from .seeds_service import SeedsService
from .vector_service import VectorService

image_file_service = ImageFileService()
image_service = ImageService()
seeds_service = SeedsService()
vector_service = VectorService()


# noinspection PyMethodMayBeStatic
class GeneratorService:
    generator = None
    batch_size = None
    random_noise = None

    def is_initialized(self) -> bool:
        """ Check if generator is initialized """
        return self.generator is not None

    def initialize(self, db: Session, batch_size: int = 1, random_noise: bool = False) -> None:
        """ Initialize the generator with provided settings """
        assert not self.is_initialized()
        self.batch_size = batch_size
        self.random_noise = random_noise
        self.generator = GeneratorWrapper(batch_size, random_noise, vector_service.get_dict(db))
        # [Necessary/Required] Dummy generation to save internal variables:
        _ = self.generator.generate(0)

    def restart(self, batch_size: int = 1, random_noise: bool = False) -> None:
        """ Restart the generator with new settings """
        assert self.is_initialized()
        self.batch_size = batch_size
        self.random_noise = random_noise
        self.generator.restart_generator(batch_size, random_noise)

    def __assert_initialization(self, db: Session, batch_size: int = 1, random_noise: bool = False):
        """ Assert the initialization of the generator. Restart only if the random noise changed or
            requested batch size is higher than current, otherwise padding takes care of it """
        if not self.is_initialized():
            self.initialize(db, batch_size, random_noise)
        elif self.batch_size < batch_size or self.random_noise != random_noise:
            self.restart(batch_size, random_noise)

    def generate_image(self, db: Session, request: GenerateRequest) -> Image:
        """ Generate an image, save the file, and register in the database """
        self.__assert_initialization(db, batch_size=1)
        vectors = [(v.id, v.multiplier) for v in request.vectors]
        rgb_3d_array = self.generator.generate(request.seed, vectors)[0]
        image_filename = image_file_service.save_generated_image(rgb_3d_array, request.seed, request.session_id)
        return image_service.create(db, request, image_filename)

    def create_research_trials(self, db: Session, session: ResearchSession, batch_size: int = 8,
                               seeds: List[int] = None) -> None:
        """ Generate a whole research session, save images, and register them in the database.
            Method generates [len(seeds) * len(vectors) * slider_steps/len(multipliers)] amount of images"""
        # Restarting the tensorflow session helps with memory overloads, hence this next line:
        self.restart(batch_size) if self.is_initialized() else self.initialize(db, batch_size)
        setting = session.research_setting
        if not seeds:
            seeds = seeds_service.get_seeds(setting.total_amount, setting.overlap_amount, setting.equalize_gender)
        vector_ids = vector_service.get_ids(db)
        multipliers = list(np.round(np.linspace(0, 1, setting.slider_steps) * setting.global_multiplier, 5))
        seeds_batches = np.array_split(seeds, math.ceil(len(seeds) / batch_size))
        for seeds_batch in seeds_batches:
            base_ls = self.generator.get_latent_states(seeds_batch)
            latent_states = self.__apply_vectors(base_ls, vector_ids, multipliers)
            images = self.__generate_batches(latent_states)
            self.__save_images(images, db, session.id, seeds_batch, vector_ids, multipliers)

    def __apply_vectors(self, latent_states, vector_ids: List[int], multipliers: List[float]):
        """ Apply vectors with different multipliers to the copies of provided latent states and accumulate.
            Result is of shape (latent_states.shape[0] * len(vectors) * len(multipliers), 18, 512) """
        accumulation = np.array([])
        for vector_id, multiplier in product(vector_ids, multipliers):
            vectorized_ls = self.generator.apply_vectors_to_latent(np.copy(latent_states), [(vector_id, multiplier)])
            accumulation = np.append(accumulation, vectorized_ls)
        return accumulation.reshape((latent_states.shape[0] * len(vector_ids) * len(multipliers), 18, 512))

    def __generate_batches(self, latent_states):
        """ Generate images in batches """
        batches = np.array_split(latent_states, math.ceil(latent_states.shape[0] / self.batch_size), axis=0)
        images = self.generator.generate_from_latent(batches[0])
        for batch in batches[1:]:
            images = np.append(images, self.generator.generate_from_latent(batch), axis=0)
        return images

    def __save_images(self, images, db: Session, session_id: int, seeds: List[int],
                      vector_ids: List[int], multipliers: List[float]) -> None:
        """ Save generated images to disk and then register to the database """
        parallel = Parallel(n_jobs=multiprocessing.cpu_count())
        filenames = parallel(delayed(image_file_service.save_generated_image)
                             (image, seed, session_id) for image, seed in zip(images, cycle(seeds)))
        # Register to the database:
        images_by_multiplier = np.array_split([v for v in zip(filenames, cycle(seeds))], len(filenames) / len(seeds))
        vector_multiplier = product(vector_ids, multipliers)
        for (images_seeds, (vector_id, multiplier)) in zip(images_by_multiplier, vector_multiplier):
            for filename, seed in images_seeds:
                db_image = m.Image(seed=seed, filename=filename, session_id=session_id)
                db_image.vectors = [m.ImageVector(vector_id=vector_id, multiplier=multiplier)]
                db.add(db_image)
        db.commit()
