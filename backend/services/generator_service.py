import string

from sqlalchemy.orm import Session

from encoder.wrapper import GeneratorWrapper
from schemas import GenerateRequest
from .image_file_service import image_file as image_file_service
from .vector_service import vector as vector_service


class GeneratorService:
    generator = None

    def initialize(self, db: Session) -> None:
        vector_effect_weight_by_id = vector_service.get_vectors_dict(db)
        self.generator = GeneratorWrapper(vector_effect_weight_by_id)
        _ = self.generator.generate(0)  # [Necessary] Dummy call to save internal variables

    def is_initialized(self) -> bool:
        return self.generator is not None

    def generate_image(self, request: GenerateRequest) -> string:
        rgb_3d_array = self.generator.generate(request.seed, request.vectors)
        return image_file_service.save_generated_image(rgb_3d_array, request.seed, request.session_id)


generator = GeneratorService()
