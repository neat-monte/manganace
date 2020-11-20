from .c_image_service import CImageService
from .generator_service import GeneratorService
from .image_file_service import ImageFileService
from .image_service import ImageService
from .research_service import ResearchService
from .seeds_service import SeedsService
from .trial_service import TrialService
from .vector_service import VectorService

# Alphabetical order

c_image = CImageService()
generator = GeneratorService()
image_file = ImageFileService()
image = ImageService()
research = ResearchService()
seeds = SeedsService()
trial = TrialService()
vector = VectorService()
