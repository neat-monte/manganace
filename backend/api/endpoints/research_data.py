from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import services
from api.background_tasks import delete_file
from api.dependencies import get_db
from api.schemas import SingleVectorData
from database import CRUD

router = APIRouter()


@router.get('/data', response_model=List[SingleVectorData])
def get_data(db: Session = Depends(get_db)) -> Any:
    return services.research.get_results_data(db)


@router.get('/data/export')
def export_data_csv(background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    filepath = services.research.export_results_data(db)
    background_tasks.add_task(delete_file, filepath=filepath)
    return FileResponse(filepath)


@router.get('/data/{research_session_id}', response_model=List[SingleVectorData])
def get_data(research_session_id: int, db: Session = Depends(get_db)) -> Any:
    db_research_session = CRUD.research_session.get(db, research_session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_results_data(db, research_session_id)