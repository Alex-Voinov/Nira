import asyncio
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties


try:
    from aiogram.fsm.storage.redis import RedisStorage
except Exception:
    RedisStorage = None

from pydantic_settings import BaseSettings


# -------------------------
# Config
# -------------------------
class Settings(BaseSettings):
    tg_token: str
    use_redis: bool = False
    redis_dsn: Optional[str] = None
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


# -------------------------
# Logging
# -------------------------
log_level = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(level=log_level,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


# -------------------------
# Create bot + storage + dispatcher
# -------------------------
def create_storage():
    if settings.use_redis and RedisStorage and settings.redis_dsn:
        logger.info("Using RedisStorage")
        return RedisStorage.from_url(settings.redis_dsn)
    logger.info("Using MemoryStorage (fallback)")
    return MemoryStorage()


async def create_dispatcher():
    bot = Bot(
        token=settings.tg_token,
        default=DefaultBotProperties(parse_mode="HTML")  # <- вот так теперь
    )
    storage = create_storage()
    dp = Dispatcher(storage=storage)
    # если используете webhook — настройте dp.startup.register(handler) и set_webhook
    return bot, dp


# -------------------------
# Example middleware (rate-limit)
# -------------------------
from aiogram.client.session.aiohttp import AiohttpSession  # optional

class SimpleRateLimitMiddleware:
    """
    Very small example middleware: blocks user if they spam.
    Replace with Redis-backed counters in prod.
    """
    def __init__(self, limit_seconds: int = 1):
        self.limit_seconds = limit_seconds
        self._last_call: dict[int, float] = {}

    async def __call__(self, handler, event, data):
        from time import time
        uid = event.from_user.id if hasattr(event, "from_user") and event.from_user else 0
        now = time()
        last = self._last_call.get(uid, 0)
        if now - last < self.limit_seconds:
            # простая защита: отменяем дальнейшую обработку
            return
        self._last_call[uid] = now
        return await handler(event, data)


# -------------------------
# Routers / Handlers
# -------------------------
router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это минимальный, но production-ready старт для aiogram 3.\n"
        "Отправь /help чтобы посмотреть возможности."
    )

@router.message(Command(commands=["help"]))
async def cmd_help(message: types.Message):
    await message.answer("Пока тут: /start, /help. Добавь свои роутеры в router(s).")


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
    # Очистка/закрытие соединений
    await bot.session.close()
    await bot.dispatcher.storage.close()
    if RedisStorage:
        await bot.dispatcher.storage.wait_closed()


# -------------------------
# Main entrypoint
# -------------------------
async def main():
    bot, dp = await create_dispatcher()

    # register router(s)
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
