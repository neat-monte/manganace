import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

import services
from api.dependencies import get_db
from database import CRUD

router = APIRouter()


@router.get('/research-session-duplicates/{research_session_id}')
def fix_research_session_duplicates(research_session_id: int, db: Session = Depends(get_db)) -> Any:
    """ Fix a research session by removing duplicates and creating new trial(s) """
    session = CRUD.research_session.get(db, research_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Research session not found")
    setting = session.research_setting
    # Find duplicate seeds
    seeds = [image.seed for image in session.images]
    dup_seeds = set([seed for seed in seeds if seeds.count(seed) > 6 * setting.slider_steps])
    # Extract duplicate images and unused images
    dup_images = [image for image in session.images if image.seed in dup_seeds]
    del_images, traces = [], []
    for image in dup_images:
        trace = (image.seed, image.vectors[0].vector_id, image.vectors[0].multiplier)
        if not image.collection_images and trace not in traces:
            del_images.append(image)
            traces.append(trace)
    if not del_images:
        raise HTTPException(status_code=404, detail='No duplicates found')
    # Delete image files with associated database images
    for image in del_images:
        filepath = services.image_file.get_path(image.filename, research_session_id)
        if os.path.exists(filepath):
            os.remove(filepath)
        CRUD.image.delete(db, image.id)
    # Select a new seed
    unique_seeds = set(seeds)
    new_seeds = services.seeds.complete_the_list(unique_seeds, setting.total_amount, setting.overlap_amount,
                                                 setting.equalize_gender)
    # Generate and register new images
    services.generator.create_research_trials(db, session, seeds=new_seeds)
    return Response(status_code=200)


@router.get('/research-session-trials/{research_session_id}')
def fix_research_session_trials(research_session_id: int, db: Session = Depends(get_db)) -> Any:
    """ Generate additional trials for a research session """
    session = CRUD.research_session.get(db, research_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Research session not found")
    setting = session.research_setting
    unique_seeds = set([image.seed for image in session.images])
    if len(unique_seeds) == setting.total_amount:
        raise HTTPException(status_code=403, detail="Research session has correct amount of trials")
    new_seeds = services.seeds.complete_the_list(unique_seeds, setting.total_amount, setting.overlap_amount,
                                                 setting.equalize_gender)
    services.generator.create_research_trials(db, session, seeds=new_seeds)
    return Response(status_code=200)
