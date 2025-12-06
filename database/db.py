from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from typing import AsyncGenerator
from logging import getLogger, WARNING


getLogger("sqlalchemy.engine").setLevel(WARNING)
engine = create_async_engine(settings.db_dsn, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
