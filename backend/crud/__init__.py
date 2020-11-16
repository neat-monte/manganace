from models import *

from .c_image import CRUDCImage
from .collection import CRUDUserCollection
from .image import CRUDImage
from .session import CRUDSession
from .session_g import CRUDSessionG
from .session_r import CRUDSessionR
from .tag import CRUDTag
from .vector import CRUDVector

# Alphabetical order

c_image = CRUDCImage(CImage)
collection = CRUDUserCollection(UserCollection)
image = CRUDImage(Image)
session = CRUDSession(Session)
session_g = CRUDSessionG(GeneratorSession)
session_r = CRUDSessionR(ResearchSession)
tag = CRUDTag(Tag)
vector = CRUDVector(Vector)
