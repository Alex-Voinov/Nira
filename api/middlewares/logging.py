import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

logger = logging.getLogger("app.middleware")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware для логирования всех запросов к FastAPI
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000  # в мс
        log_message = (
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"time={process_time:.2f}ms"
        )

        if response.status_code >= 500:
            logger.error(log_message)
        elif response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response
