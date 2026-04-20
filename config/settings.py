from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BASE_URL: str = "https://jsonplaceholder.typicode.com"
    API_TIMEOUT: int = 30
    RETRY_COUNT: int = 3
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()