from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any


class SimpleRateLimitMiddleware:
    """
    Rate-limit middleware.
    В продакшене рекомендуется Redis-backed хранилище.
    """

    def __init__(self, limit_seconds: int = 1):
        self.limit_seconds = limit_seconds
        self._last_call: dict[int, float] = {}

    async def __call__(self, handler, event: Message, data: dict):
        from time import time
        uid = event.from_user.id if event.from_user else 0
        now = time()
        last = self._last_call.get(uid, 0)
        if now - last < self.limit_seconds:
            return  # блокируем повторный вызов
        self._last_call[uid] = now
        return await handler(event, data)


class MessageLogMiddleware(BaseMiddleware):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[Any, dict], Awaitable[Any]],
        event,
        data: dict
    ):
        result = await handler(event, data)

        user = data.get("event_from_user")

        if hasattr(result, "message_id") and user:
            self.storage.add(user.id, result.message_id)

        return result
