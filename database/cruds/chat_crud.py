from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session
from .models import User, Photo, Message, Chat, Group, Like, Dislike

async def get_chat_by_users(user_id: int, target_id: int, limit=50, offset=0):
    """Получить чат между двумя пользователями"""
    async with async_session() as session:
        stmt = select(Chat).where(
            ((Chat.user_id == user_id) & (Chat.target_id == target_id)) |
            ((Chat.user_id == target_id) & (Chat.target_id == user_id))
        ).order_by(Chat.id.desc()).limit(limit).offset(offset)
        result = await session.execute(stmt)
        chats = result.scalars().all()
        # достать сообщения
        messages = []
        for chat in chats:
            msg = await session.get(Message, chat.message_id)
            messages.append(msg)
        return messages