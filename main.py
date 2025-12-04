import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from config import settings
from bot.middlewares.ratelimit import SimpleRateLimitMiddleware
from bot.handlers import router
from database import engine, Base


try:
    from aiogram.fsm.storage.redis import RedisStorage
except Exception:
    RedisStorage = None

# Logging
log_level = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def create_storage():
    """Выбираем хранилище FSM."""
    if settings.use_redis:
        if not RedisStorage or not settings.redis_dsn:
            raise RuntimeError(
                "RedisStorage запрошен, но пакет или DSN отсутствуют!")
        logger.info("Using RedisStorage")
        return RedisStorage.from_url(settings.redis_dsn)
    logger.info("Using MemoryStorage (fallback)")
    return MemoryStorage()


async def on_startup(dp: Dispatcher):
    logger.info("Startup: initializing resources")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown(dp: Dispatcher, bot: Bot):
    logger.info("Shutdown: releasing resources")
    await bot.session.close()
    await dp.storage.close()
    if RedisStorage:
        await dp.storage.wait_closed()


async def handle_errors(update, exception):
    logger.exception("Unhandled exception: %s", exception)


async def main():
    storage = create_storage()
    bot = Bot(token=settings.tg_token,
              default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    dp.message.middleware(SimpleRateLimitMiddleware(limit_seconds=1))
    dp.errors.register(handle_errors)

    # Регистрация startup/shutdown без лямбд
    async def startup_handler(*args, **kwargs):
        await on_startup(dp)

    async def shutdown_handler(*args, **kwargs):
        await on_shutdown(dp, bot)

    dp.startup.register(startup_handler)
    dp.shutdown.register(shutdown_handler)

    try:
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Got stop signal")
    except Exception as e:
        logger.error(e)
    finally:
        await on_shutdown(dp, bot)

if __name__ == "__main__":
    asyncio.run(main())
