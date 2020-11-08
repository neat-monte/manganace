from typing import Generator

from database import LocalSession


# noinspection PyUnboundLocalVariable
def get_db() -> Generator:
    """ Provides with a database dependency, closes connection after endpoint has completed """
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
