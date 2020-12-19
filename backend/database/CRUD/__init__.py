from database.models import *
from .collection_image import CRUDCollectionImage
from .generator_session import CRUDGeneratorSession
from .image import CRUDImage
from .participant import CRUDParticipant
from .participant_collection import CRUDParticipantCollection
from .research_session import CRUDResearchSession
from .research_setting import CRUDResearchSetting
from .tag import CRUDTag
from .trial_pick import CRUDTrialPick
from .user_collection import CRUDUserCollection
from .vector import CRUDVector

# Alphabetical order

collection_image = CRUDCollectionImage(CImage)
generator_session = CRUDGeneratorSession(GeneratorSession)
image = CRUDImage(Image)
participant = CRUDParticipant(Participant)
participant_collection = CRUDParticipantCollection(ParticipantCollection)
research_session = CRUDResearchSession(ResearchSession)
research_setting = CRUDResearchSetting(ResearchSetting)
tag = CRUDTag(Tag)
trial_pick = CRUDTrialPick(TrialPick)
user_collection = CRUDUserCollection(UserCollection)
vector = CRUDVector(Vector)
