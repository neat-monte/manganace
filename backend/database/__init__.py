from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.DATABASE_CONNECTION_STRING, connect_args={"check_same_thread": False})

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
