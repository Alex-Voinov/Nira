# Middleware для проверки подлинности Telegram WebApp запросов

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from hmac import new
from hashlib import sha256
from urllib.parse import parse_qsl
from json import JSONDecodeError, loads


from config import settings

BOT_TOKEN: str | None = settings.tg_token


def validate_telegram_init_data(init_data: str) -> dict | None:
    """
    Проверяет подлинность initData от Telegram WebApp.

    Возвращает:
    - dict с данными Telegram (user, auth_date и т.д.) → если подпись валидна
    - None → если подпись невалидна
    """

    # ✅ Превращаем query-строку в словарь
    parsed_data: dict = dict(parse_qsl(init_data))

    # ✅ Забираем hash, без него проверка невозможна
    received_hash: str | None = parsed_data.pop("hash", None)

    if not received_hash:
        return None

    # ✅ Собираем строку для проверки подписи:
    # key=value\nkey=value\n...
    data_check_string: str = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed_data.items())
    )

    # ✅ Генерируем секретный ключ из BOT_TOKEN
    secret_key: bytes = sha256(BOT_TOKEN.encode()).digest()

    # ✅ Генерируем хеш на сервере
    calculated_hash: str = new(
        secret_key,
        data_check_string.encode(),
        sha256,
    ).hexdigest()

    # ❌ Хеши не совпали → запрос поддельный
    if calculated_hash != received_hash:
        return None

    # ✅ Безопасно парсим пользователя (НИКАКОГО eval)
    if "user" in parsed_data:
        try:
            parsed_data["user"] = loads(parsed_data["user"])
        except JSONDecodeError:
            return None

    return parsed_data


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware, которое:
    - работает на КАЖДОМ запросе
    - проверяет x-telegram-init-data
    - валидирует подпись
    - кладёт пользователя в request.state.telegram_user
    """

    async def dispatch(self, request: Request, call_next):
        # ✅ Проверяем, что BOT_TOKEN вообще задан
        if not BOT_TOKEN:
            return JSONResponse(
                {"detail": "BOT_TOKEN is not configured"},
                status_code=500,
            )

        # ✅ Достаём initData из заголовка
        init_data: str | None = request.headers.get("x-telegram-init-data")

        if not init_data:
            return JSONResponse(
                {"detail": "Missing x-telegram-init-data header"},
                status_code=401,
            )

        # ✅ Проверяем подпись Telegram
        telegram_data: dict | None = validate_telegram_init_data(init_data)

        if not telegram_data:
            return JSONResponse(
                {"detail": "Invalid telegram init data"},
                status_code=401,
            )

        # ✅ Кладём пользователя в request.state
        request.state.telegram_user = telegram_data.get("user")

        # ✅ Пропускаем запрос дальше
        response = await call_next(request)
        return response
