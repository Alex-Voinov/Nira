import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from config import settings
from middlewares.ratelimit import SimpleRateLimitMiddleware
from handlers import router


try:
    from aiogram.fsm.storage.redis import RedisStorage
except Exception:
    RedisStorage = None


# -------------------------
# Logging
# -------------------------
log_level = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------
# Create bot + storage + dispatcher
# -------------------------
def create_storage():
    """
    Создание хранилища для FSM:
    Redis если доступен и указан DSN, иначе MemoryStorage.
    """
    if settings.use_redis:
        if not RedisStorage or not settings.redis_dsn:
            raise RuntimeError("RedisStorage запрошен, но пакет или DSN отсутствуют!")
        logger.info("Using RedisStorage")
        return RedisStorage.from_url(settings.redis_dsn)
    logger.info("Using MemoryStorage (fallback)")
    return MemoryStorage()


# Global error handler
async def handle_errors(update, exception):
    logger.exception("Unhandled exception: %s", exception)
    # можно отправлять в Sentry / журнал и т.д.


# -------------------------
# Startup / Shutdown
# -------------------------
async def on_startup(bot: Bot):
    logger.info("Startup: initializing resources")
    # Примеры: подключение к базе, миграции, регистрация webhook, etc.
    # Если webhook:
    # await bot.set_webhook("https://example.com/telegram/webhook")
    # dp['db'] = db_connection  # можно положить общие ресурсы в dp.storage/ dp.data


async def on_shutdown(bot: Bot):
    logger.info("Shutdown: releasing resources")
    await bot.session.close()
    await bot.dispatcher.storage.close()
    if RedisStorage:
        await bot.dispatcher.storage.wait_closed()


# -------------------------
# Main entrypoint
# -------------------------
async def main():
    storage = create_storage()

    async with Bot(
        token=settings.tg_token,
        default=DefaultBotProperties(parse_mode="HTML")
    ) as bot:
        dp = Dispatcher(storage=storage)
        dp.include_router(router)

        # register middleware
        dp.message.middleware(SimpleRateLimitMiddleware(limit_seconds=1))

        # error / events
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        dp.errors.register(handle_errors)

        # Запуск: polling (для вебхуков настройка другая)
        try:
            logger.info("Starting polling...")
            await dp.start_polling(bot)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Got stop signal")
        finally:
            # надёжный shutdown
            await on_shutdown(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
