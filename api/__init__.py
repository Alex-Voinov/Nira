from fastapi import FastAPI
from api.routers.router import router as api_router
from api.middlewares.logging import LoggingMiddleware
from logger import logger
from fastapi.staticfiles import StaticFiles
from config import BUILD_DIR


app = FastAPI()
app.add_middleware(LoggingMiddleware)

# API
app.include_router(api_router, prefix="/api")

app.mount("/", StaticFiles(directory=BUILD_DIR, html=True), name="frontend")

logger.info("FastAPI app created")