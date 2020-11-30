import multiprocessing
from itertools import product, cycle, islice

import numpy as np
from joblib import Parallel, delayed
from sqlalchemy.orm import Session

import database.models as m
from api.schemas import GenerateRequest, Image, ImageVector
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


class GeneratorService:
    def __init__(self):
        self.generator = None
        self.batch_size = None
        self.random_noise = None

    def initialize(self, db: Session, batch_size: int = 1, random_noise: bool = False) -> None:
        if self.is_initialized():
            return
        self.batch_size = batch_size
        self.random_noise = random_noise
        self.generator = GeneratorWrapper(batch_size, random_noise, vector_service.get_dict(db))
        # [Necessary] Dummy call to save internal variables:
        _ = self.generator.generate_from_latent(np.zeros((self.batch_size, 18, 512)))

    def shutdown(self):
        if not self.is_initialized():
            return
        self.generator.shutdown()
        self.generator = None

    def is_initialized(self) -> bool:
        return self.generator is not None

    def generate_image(self, db: Session, request: GenerateRequest) -> Image:
        if not self.is_initialized():
            self.initialize(db)
        vectors = [(v.id, v.multiplier) for v in request.vectors]
        rgb_3d_array = self.generator.generate(request.seed, vectors)[0]
        image_filename = image_file_service.save_generated_image(rgb_3d_array, request.seed, request.session_id)
        return image_service.create(db, request, image_filename)

    def create_research_trials(self, db: Session, session: ResearchSession, batch_size: int = 10):
        if not self.is_initialized() or self.batch_size != batch_size:
            self.shutdown()
            self.initialize(db, batch_size)
        seeds = seeds_service.get_seeds(session.total_amount, session.overlap_amount, session.equalize_gender)
        vector_ids = vector_service.get_ids(db)
        multipliers = np.linspace(0, 1, session.slider_steps)
        # Get base latent states of all seeds with shape of (len(seeds), 18, 512):
        base_ls = self.generator.get_latent_states(seeds)
        # Apply vectors to the copies of base latent states and accumulate
        # with shape of (len(seed) * len(vectors) * len(multipliers) * 18 * 512) due to initial empty list:
        ls = np.array([])
        for vector_id, multiplier in product(vector_ids, multipliers):
            vectorized_ls = self.generator.apply_vectors_to_latent(np.copy(base_ls), [(vector_id, multiplier)])
            ls = np.append(ls, vectorized_ls)
        # Reshape and split into batches of the selected batch size:
        ls = ls.reshape((len(seeds) * len(vector_ids) * len(multipliers), 18, 512))
        batches = np.array_split(ls, ls.shape[0] / batch_size, axis=0)
        # Generate and accumulate images:
        images = self.generator.generate_from_latent(batches[0])
        for batch in batches[1:]:
            images = np.append(images, self.generator.generate_from_latent(batch), axis=0)
        # Save image files to disk (FYI: filenames are kept in order even after parallel computation):
        filenames = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(image_file_service.save_generated_image)
                                                                 (image, seed, session.id)
                                                                 for image, seed in zip(images, cycle(seeds)))
        # Save images to the database:
        images_by_multiplier = np.array_split([v for v in zip(filenames, cycle(seeds))], len(filenames) / len(seeds))
        for vector_id, multiplier in product(vector_ids, multipliers):
            for filename, seed in images_by_multiplier:
                db_image = m.Image(seed=seed, filename=filename, session_id=session.id)
                db_image.vectors = [m.ImageVector(vector_id=vector_id, multiplier=multiplier)]
                db.add(db_image)
        db.commit()

    # def test(self, db: Session):
    #     seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    #               16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        # base_seeds_ls = self.generator.get_latent_states(seeds)
    #     vector_ids = vector_service.get_ids(db)
    #     multipliers = np.linspace(0, 1, 11)
    #     ls = np.array([])
    #     for vector_id, multiplier in product(vector_ids, multipliers):
    #         vectorized_ls = self.generator.apply_vectors_to_latent(np.copy(base_seeds_ls), [(vector_id, multiplier)])
    #         ls = np.append(ls, vectorized_ls)
    #     ls = ls.reshape((len(seeds) * len(vector_ids) * len(multipliers), 18, 512))
    #     batches = np.array_split(ls, ls.shape[0] / 10, axis=0)
    #     images = self.generator.generate_from_latent(batches[0])
    #     for batch in batches[1:]:
    #         images = np.append(images, self.generator.generate_from_latent(batch), axis=0)
    #     filenames = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(image_file_service.save_generated_image)
    #                                                              (image, seed, 99)
    #                                                              for image, seed in zip(images, cycle(seeds)))
    #     print(filenames)
