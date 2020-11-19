from models import *

from .c_image import CRUDCImage
from .collection_p import CRUDParticipantCollection
from .collection_u import CRUDUserCollection
from .image import CRUDImage
from .participant import CRUDParticipant
from .session_g import CRUDSessionG
from .session_r import CRUDSessionR
from .tag import CRUDTag
from .vector import CRUDVector

# Alphabetical order

c_image = CRUDCImage(CImage)
collection_u = CRUDUserCollection(UserCollection)
collection_p = CRUDParticipantCollection(ParticipantCollection)
image = CRUDImage(Image)
participant = CRUDParticipant(Participant)
session_g = CRUDSessionG(GeneratorSession)
session_r = CRUDSessionR(ResearchSession)
tag = CRUDTag(Tag)
vector = CRUDVector(Vector)
