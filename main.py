import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from config import settings
from bot.middlewares.ratelimit import SimpleRateLimitMiddleware
from bot.handlers import router as bot_router
from database import engine, Base

from fastapi import FastAPI
from api.router.router import router as api_router
import uvicorn

try:
    from aiogram.fsm.storage.redis import RedisStorage
except Exception:
    RedisStorage = None

# =========================
# Logging
# =========================
log_level = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# =========================
# FastAPI app
# =========================
app = FastAPI()
app.include_router(api_router, prefix="/api")

# =========================
# FSM Storage
# =========================
def create_storage():
    if settings.use_redis:
        if not RedisStorage or not settings.redis_dsn:
            raise RuntimeError(
                "RedisStorage запрошен, но пакет или DSN отсутствуют!"
            )
        logger.info("Using RedisStorage")
        return RedisStorage.from_url(settings.redis_dsn)
    logger.info("Using MemoryStorage (fallback)")
    return MemoryStorage()

# =========================
# Создание таблиц
# =========================
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

# =========================
# Запуск бота
# =========================
async def start_bot():
    storage = create_storage()
    bot = Bot(token=settings.tg_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.include_router(bot_router)

    dp.message.middleware(SimpleRateLimitMiddleware(limit_seconds=1))

    async def handle_errors(update, exception):
        logger.exception("Unhandled exception: %s", exception)

    dp.errors.register(handle_errors)

    # создаём таблицы до запуска бота
    await create_tables()

    logger.info("Starting bot polling...")
    await dp.start_polling(bot)

# =========================
# Запуск FastAPI
# =========================
async def start_api():
    config = uvicorn.Config(app, host=settings.host, port=settings.port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# =========================
# Главная функция
# =========================
async def main():
    await asyncio.gather(
        start_bot(),
        start_api()
    )

if __name__ == "__main__":
    asyncio.run(main())
