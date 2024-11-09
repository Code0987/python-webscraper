from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str

    AMQP_URL: str
    AMQP_SCRAPPER_QUEUE: str

    AUTH_TOKEN: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
