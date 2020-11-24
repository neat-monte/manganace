from typing import Any

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

import data
import services
from api.background_tasks import delete_file
from api.dependencies import get_db
from schemas import Image

router = APIRouter()


@router.delete("/{id_}", response_model=Image)
def delete_image(id_: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    """ Delete an image, only deletes if no collection is dependent on it """
    db_image = data.image.get(db, id_)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    if db_image.c_images:
        raise HTTPException(status_code=403, detail="Image is being used in at least one collection")
    filepath = services.image_file.get_path(db_image.filename, db_image.session_id)
    background_tasks.add_task(delete_file, filepath=filepath)
    return services.image.delete(db, db_image)
