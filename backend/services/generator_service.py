import numpy as np
from sqlalchemy.orm import Session

from encoder.wrapper import GeneratorWrapper
from models import ResearchSession
from schemas import GenerateRequest, Image, ImageVector
from .image_file_service import ImageFileService
from .image_service import ImageService
from .seeds_service import SeedsService
from .vector_service import VectorService

image_file_service = ImageFileService()
image_service = ImageService()
seeds_service = SeedsService()
vector_service = VectorService()


class GeneratorService:
    generator = None

    def initialize(self, db: Session) -> None:
        self.generator = GeneratorWrapper(vector_service.get_dict(db))
        _ = self.generator.generate(0)  # [Necessary] Dummy call to save internal variables

    def is_initialized(self) -> bool:
        return self.generator is not None

    def generate_image(self, db: Session, request: GenerateRequest) -> Image:
        rgb_3d_array = self.generator.generate(request.seed, request.vectors)
        image_filename = image_file_service.save_generated_image(rgb_3d_array, request.seed, request.session_id)
        return image_service.create(db, request, image_filename)

    def create_research_trials(self, db: Session, session: ResearchSession):
        seeds = seeds_service.get_seeds(session.total_amount, session.overlap_amount, session.equalize_gender)
        vector_ids = vector_service.get_ids(db)
        multipliers = np.linspace(0, 1, session.slider_steps)
        for seed in seeds:
            for vector_id in vector_ids:
                for multiplier in multipliers:
                    vector = ImageVector.construct(id=vector_id, multiplier=multiplier)
                    request = GenerateRequest.construct(session_id=session.id, seed=seed, vectors=[vector])
                    self.generate_image(db, request)
