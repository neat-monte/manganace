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


@router.get('/{research_setting_id}/data', response_model=List[SingleVectorData])
def get_data(research_setting_id: int, db: Session = Depends(get_db)) -> Any:
    return services.research.get_results_data(db, research_setting_id)


@router.get('/{research_setting_id}/data/export')
def export_data_csv(background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    filepath = services.research.export_results_data(db)
    background_tasks.add_task(delete_file, filepath=filepath)
    return FileResponse(filepath)


@router.get('/{research_setting_id}/data/{research_session_id}', response_model=List[SingleVectorData])
def get_session_data(research_setting_id: int, research_session_id: int, db: Session = Depends(get_db)) -> Any:
    db_research_session = CRUD.research_session.get(db, research_session_id)
    if not db_research_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return services.research.get_results_data(db, research_setting_id, research_session_id)
