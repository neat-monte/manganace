from fastapi import APIRouter

from .endpoints import generator, collections, c_images, tags, g_sessions

main_router = APIRouter()
main_router.include_router(generator.router, prefix="/generator", tags=["GAN Generator"])
main_router.include_router(g_sessions.router, prefix="/sessions", tags=["Sessions"])
main_router.include_router(collections.router, prefix="/collections", tags=["Collections"])
main_router.include_router(c_images.router, prefix="/images", tags=["Collection images"])
main_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
