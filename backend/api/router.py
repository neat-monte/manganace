from fastapi import APIRouter

from .endpoints import generator, collections, collection_images, tags, generator_sessions, research_trials, extras, \
    images, research_setting, research_sessions, research_data, research_participant

main_router = APIRouter()
main_router.include_router(generator.router, prefix="/generator", tags=["GAN Generator"])

main_router.include_router(research_data.router, prefix="/research", tags=["Research data"])

main_router.include_router(research_trials.router, prefix="/research", tags=["Research trials"])

main_router.include_router(research_participant.router, prefix="/research", tags=["Research participants"])

main_router.include_router(research_setting.router, prefix="/research", tags=["Research settings"])

main_router.include_router(research_sessions.router, prefix="/sessions", tags=["Research sessions"])

main_router.include_router(generator_sessions.router, prefix="/sessions", tags=["Generator sessions"])

main_router.include_router(images.router, prefix="/sessions", tags=["Images (any session)"])

main_router.include_router(collections.router, prefix="/collections", tags=["User collections"])

main_router.include_router(collection_images.router, prefix="/collections", tags=["Collection images & trial picks"])

main_router.include_router(tags.router, prefix="/tags", tags=["Tags"])

main_router.include_router(extras.router, prefix="/extras", tags=["Extras"])
