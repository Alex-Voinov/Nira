from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    tg_token: str
    use_redis: bool = False
    redis_dsn: Optional[str] = None
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()