from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import data
from api.dependencies import get_db
from schemas import Tag, TagCreate, TagUpdate

router = APIRouter()


@router.post('/', response_model=Tag)
def create_tag(tag_in: TagCreate, db: Session = Depends(get_db)) -> Any:
    """ Create a new tag """
    return data.tag.create(db, tag_in)


@router.get('/', response_model=List[Tag])
def get_tags(db: Session = Depends(get_db)) -> Any:
    """ Get a list of all tags """
    return data.tag.get_all(db)


@router.get("/research", response_model=List[Tag])
def get_research_tags(db: Session = Depends(get_db)) -> Any:
    """ Get a list of available education options """
    return data.tag.get_all_research(db)


@router.get("/{id_}", response_model=Tag)
def get_tag(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Get a tag by id """
    tag = data.tag.get(db, id_)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put('/{id_}', response_model=Tag)
def update_tag(id_: int, tag_in: TagUpdate, db: Session = Depends(get_db)) -> Any:
    """ Modify an existing tag """
    tag = data.tag.get(db, id_)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return data.tag.update(db, tag, tag_in)


@router.delete("/{id_}", response_model=Tag)
def delete_tag(id_: int, db: Session = Depends(get_db)) -> Any:
    """ Delete a tag """
    tag = data.tag.get(db, id_)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if tag.for_research:
        raise HTTPException(status_code=403, detail="Tag is hidden and immutable")
    return data.tag.delete(db, id_)
