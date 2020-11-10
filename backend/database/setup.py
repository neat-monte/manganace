import json
from pathlib import Path

from sqlalchemy.orm import Session

from models.vector import Vector
from . import LocalSession, Base, engine

SETUP_DATA = Path.cwd() / "_preexisting_data"
VECTORS = SETUP_DATA / "vectors.json"


def database_setup():
    """ Create database with tables and populate or update it """
    Base.metadata.create_all(bind=engine)
    db = LocalSession()
    try:
        populate_vectors(db)
    finally:
        db.close()


def populate_vectors(db: Session):
    """ Read the JSON file and populate emotions table or update weights """
    with open(VECTORS, "r") as file:
        vectors = json.loads(file.read())
    for vector in vectors:
        vector_db = db.query(Vector).filter(Vector.name == vector["name"]).first()
        if vector_db:
            if vector_db.weight != vector["weight"]:
                vector_db.weight = vector["weight"]
            continue
        db.add(Vector(**vector))
    db.commit()
