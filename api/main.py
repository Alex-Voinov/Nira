from fastapi import FastAPI
from uvicorn import run

from config import settings
from fastapi.middleware.cors import CORSMiddleware
from api.routers.routers_get import router as get_router
from api.routers.routers_post import router as post_router
from api.middlewares.logging import LoggingMiddleware
from logger import logger


def get_app() -> FastAPI:
    app = FastAPI(debug=settings.debug)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
    CORSMiddleware,
        allow_origins=[settings.web_app_url],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )
    app.include_router(get_router, prefix="/api")
    app.include_router(post_router, prefix="/api")
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
