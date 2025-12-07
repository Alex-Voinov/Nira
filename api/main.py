from fastapi import FastAPI
from uvicorn import run

from config import settings
from api.routers.router import router as api_router
from api.middlewares.logging import LoggingMiddleware
from logger import logger

def get_app() -> FastAPI:
    app = FastAPI(debug=settings.debug)
    app.add_middleware(LoggingMiddleware)
    app.include_router(api_router, prefix="/api")
    logger.info("FastAPI app created")
    return app

app = get_app()

# ===== Точка входа =====
if __name__ == "__main__":
    run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="debug" if settings.debug else "info",
    )
