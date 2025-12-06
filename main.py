# 1. Стандартная библиотека
from asyncio import gather, run, create_task
from subprocess import run as process_run, CalledProcessError
from shutil import which

# 2. Сторонние библиотеки
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from uvicorn import Config, Server

# 3. Локальные модули
from config import settings, FRONTEND_DIR
from bot.middlewares.ratelimit import SimpleRateLimitMiddleware
from bot.handlers import router as bot_router
from database import engine, Base
from api import app
from logger import logger

try:
    from aiogram.fsm.storage.redis import RedisStorage
except Exception:
    RedisStorage = None

# =========================
# Функция сборки фронтенда
# =========================
def build_frontend():
    if not settings.build_frontend:
        logger.info("Frontend build skipped (build_frontend=False)")
        return

    logger.info("🔨 Starting frontend build...")

    # ищем git bash
    git_bash_path = which("bash")
    use_git_bash = git_bash_path is not None

    commands = [
        "npm install",
        "npm run build"
    ]

    for cmd in commands:
        try:
            if use_git_bash:
                logger.info(f"Executing with Git Bash: {cmd}")
                process_run([git_bash_path, "-c", cmd], cwd=FRONTEND_DIR, check=True)
            else:
                logger.info(f"Executing with shell fallback: {cmd}")
                process_run(cmd, cwd=FRONTEND_DIR, check=True, shell=True)
        except CalledProcessError as e:
            logger.warning(f"Frontend build command failed: {cmd}\n{e}")
        except FileNotFoundError as e:
            logger.warning(f"Command not found: {cmd}\n{e}")

    logger.info("✅ Frontend build finished (check logs for errors)")


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
    logger.warning("Using MemoryStorage (fallback)")
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
    config = Config(app, host=settings.host, port=settings.port, log_level="info")
    server = Server(config)
    await server.serve()

# =========================
# Главная функция
# =========================
async def main():
    api_task = create_task(start_api())
    bot_task = create_task(start_bot())
    await gather(api_task, bot_task)

if __name__ == "__main__":
    build_frontend()
    run(main())
