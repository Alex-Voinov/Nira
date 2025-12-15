from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from init_data_py import InitData
from config import settings

BOT_TOKEN: str | None = settings.tg_token


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки Telegram WebApp init_data через init-data-py
    """

    async def dispatch(self, request: Request, call_next):
        if not BOT_TOKEN:
            return JSONResponse(
                {"detail": "BOT_TOKEN is not configured"},
                status_code=500,
            )

        # В dev можно передавать данные альтернативным заголовком без шифрования
        if settings.mode == "dev":
            init_data_raw = request.headers.get("x-telegram-init-data") \
                            or request.headers.get("x-telegram-dev-data")
            if not init_data_raw:
                # В dev можно даже пропускать данные
                request.state.telegram_user = None
                return await call_next(request)

            # Если данные есть, пробуем парсить, но не валидируем подпись
            try:
                init_data_obj = InitData.parse(init_data_raw)
                request.state.telegram_user = init_data_obj.user
            except Exception:
                # Если не удалось распарсить, просто игнорируем в dev
                request.state.telegram_user = None

            return await call_next(request)

        init_data_raw: str | None = request.headers.get("x-telegram-init-data")
        if not init_data_raw:
            return JSONResponse(
                {"detail": "Missing x-telegram-init-data header"},
                status_code=401,
            )

        # ✅ Парсим init_data через библиотеку
        try:
            init_data_obj = InitData.parse(init_data_raw)
        except Exception as e:
            return JSONResponse(
                {"detail": "Invalid init_data format"},
                status_code=401,
            )

        # ✅ Валидируем подпись и срок жизни
        try:
            is_valid = init_data_obj.validate(bot_token=BOT_TOKEN, lifetime=3600)
            if not is_valid:
                return JSONResponse(
                    {"detail": "Invalid or expired telegram init data"},
                    status_code=401,
                )
        except Exception as e:
            return JSONResponse(
                {"detail": "Validation error"},
                status_code=401,
            )

        # ✅ Кладём пользователя в request.state
        request.state.telegram_user = init_data_obj.user

        response = await call_next(request)
        return response
