from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import CRUD
from api.dependencies import get_db
from api.schemas import ResearchSetting, ResearchSettingCreate

router = APIRouter()


@router.get('/', response_model=List[ResearchSetting])
def get_research_settings(db: Session = Depends(get_db)) -> Any:
    """ Get a list of all research settings """
    return CRUD.research_setting.get_all(db)


@router.post('/', response_model=ResearchSetting)
def create_research_setting(setting_in: ResearchSettingCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new research setting """
    return CRUD.research_setting.create(db, setting_in)


@router.delete("/{id_}", response_model=ResearchSetting)
def delete_research_setting(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a research setting """
    db_research_setting = CRUD.research_setting.get(db, id_)
    if not db_research_setting:
        raise HTTPException(status_code=404, detail="Research setting not found")
    if db_research_setting.research_sessions:
        raise HTTPException(status_code=403, detail="Research setting has sessions")
    return CRUD.research_setting.delete(db, id_)
