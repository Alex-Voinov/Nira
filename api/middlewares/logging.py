# logging_middleware.py
# Расширенное логирование всех запросов FastAPI

from time import time
from logging import getLogger

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


logger = getLogger("app.middleware")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Production middleware для логирования:
    - метода
    - пути
    - статуса
    - времени выполнения
    - IP
    - User-Agent
    - Telegram user id (если есть)
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time()

        try:
            response = await call_next(request)
        except Exception as exc:
            # ✅ Если упал необработанный exception — логируем как 500
            process_time = (time() - start_time) * 1000

            ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")

            logger.exception(
                f"{request.method} {request.url.path} "
                f"status=500 "
                f"time={process_time:.2f}ms "
                f"ip={ip} "
                f"ua='{user_agent}' "
                f"error={str(exc)}"
            )
            raise

        process_time = (time() - start_time) * 1000

        # ✅ Безопасно достаём Telegram-пользователя
        tg_user = getattr(request.state, "telegram_user", None)
        tg_user_id = tg_user.get("id") if isinstance(tg_user, dict) else None

        ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        log_message = (
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"time={process_time:.2f}ms "
            f"ip={ip} "
            f"tg_id={tg_user_id} "
            f"ua='{user_agent}'"
        )

        if response.status_code >= 500:
            logger.error(log_message)
        elif response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response
