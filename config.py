from pydantic_settings import BaseSettings
from typing import Optional
from os import getenv


class Settings(BaseSettings):
    tg_token: str
    use_redis: bool = False
    redis_dsn: Optional[str] = None
    debug: bool = False
    db_dsn: str
    web_app_url: str
    port: int
    host: str
    mode: str = getenv("ENV", "dev")

    class Config:
        env_file = f".env.{getenv('ENV', 'dev')}"
        env_file_encoding = "utf-8"


settings = Settings()