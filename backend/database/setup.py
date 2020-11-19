import json
from pathlib import Path
from typing import TypeVar

from sqlalchemy.orm import Session

from models import Tag
from models.education import Education
from models.gender import Gender
from models.vector import Vector
from . import LocalSession, Base, engine

SETUP_DATA = Path.cwd() / "_setup_data"
VECTORS = SETUP_DATA / "vectors.json"
GENDERS = SETUP_DATA / "genders.json"
EDUCATIONS = SETUP_DATA / "educations.json"
TAGS = SETUP_DATA / "tags.json"


def database_setup():
    """ Create database with tables and populate or update it """
    Base.metadata.create_all(bind=engine)
    db = LocalSession()
    try:
        populate_from_json(db, Vector, str(VECTORS))
        populate_from_json(db, Gender, str(GENDERS))
        populate_from_json(db, Education, str(EDUCATIONS))
        populate_from_json(db, Tag, str(TAGS))
    finally:
        db.close()


DatabaseModel = TypeVar("DatabaseModel", bound=Base)


def populate_from_json(db: Session, model: DatabaseModel, json_file: str):
    """ Read the JSON file and populate provided model table if table is empty """
    data_exists = db.query(model).first()
    if data_exists:
        return
    with open(json_file, "r") as file:
        data = json.loads(file.read())
        for obj in data:
            db.add(model(**obj))
    db.commit()
