from fastapi import APIRouter

from .endpoints import generator, collections, c_images, tags, generator_sessions, research, extras

main_router = APIRouter()
main_router.include_router(generator.router, prefix="/generator", tags=["GAN Generator"])
main_router.include_router(research.router, prefix="/research", tags=["Research"])
main_router.include_router(generator_sessions.router, prefix="/sessions", tags=["Generator sessions"])
main_router.include_router(collections.router, prefix="/collections", tags=["User collections"])
main_router.include_router(c_images.router, prefix="/images", tags=["Collection images"])
main_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
main_router.include_router(extras.router, prefix="/extras", tags=["Extra"])
