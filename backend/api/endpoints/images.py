from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

import database.models as m
import services
from api.background_tasks import delete_file
from api.dependencies import get_db
from api.schemas import Image
from database import CRUD

router = APIRouter()


@router.get('/{session_id}/images', response_model=List[Image])
def get_session_images(session_id: int, db: Session = Depends(get_db)) -> Any:
    """ Gets all images of any session by id """
    session = db.query(m.Session).get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.image.get_all_of_session(db, session_id)


@router.delete("/images/{id_}", response_model=Image)
def delete_image(id_: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    """ Delete an image, only deletes if no collection is dependent on it """
    db_image = CRUD.image.get(db, id_)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    if db_image.collection_images:
        raise HTTPException(status_code=403, detail="Image is being used in at least one collection")
    filepath = services.image_file.get_path(db_image.filename, db_image.session_id)
    background_tasks.add_task(delete_file, filepath=filepath)
    return services.image.delete(db, db_image)
