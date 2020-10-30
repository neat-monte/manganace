from fastapi import APIRouter

from .endpoints import generator, collections, images, tags

main_router = APIRouter()
main_router.include_router(generator.router, prefix="/generator", tags=["GAN Generator"])
main_router.include_router(collections.router, prefix="/collections", tags=["Collections"])
main_router.include_router(images.router, prefix="/images", tags=["Images"])
main_router.include_router(tags.router, prefix="/tags", tags=["Tags"])
