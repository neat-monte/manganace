from typing import List, Union

from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    BACKEND_HOST_DOMAIN: str
    BACKEND_HOST_PORT: int
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_CONNECTION_STRING: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
