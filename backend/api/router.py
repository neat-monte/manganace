from fastapi import APIRouter

from .endpoints import generator, collections, collection_images, tags, generator_sessions, research

main_router = APIRouter()
main_router.include_router(generator.router, prefix="/generator", tags=["GAN Generator"])
main_router.include_router(research.router, prefix="/research", tags=["Research"])
main_router.include_router(generator_sessions.router, prefix="/sessions", tags=["Generator sessions"])
main_router.include_router(collections.router, prefix="/collections", tags=["User collections"])
main_router.include_router(collection_images.router, prefix="/images", tags=["Collection images"])
main_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
