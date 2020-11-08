import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.router import main_router
from config import settings
from database.setup import database_setup

database_setup()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.BACKEND_HOST_DOMAIN, port=settings.BACKEND_HOST_PORT)
