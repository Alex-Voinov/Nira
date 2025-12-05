from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session
from .models import User, Photo, Message, Chat, Group, Like, Dislike


async def create_group(name: str, tg_ids: list[int]):
    """Создать группу"""
    async with async_session() as session:
        async with session.begin():
            # храним как JSON строку
            group = Group(name=name, tg_ids=str(tg_ids))
            session.add(group)
            await session.commit()
            return group


async def get_group_messages(group_id: int, limit=50, offset=0):
    """Получить сообщения группы"""
    async with async_session() as session:
        group = await session.get(Group, group_id)
        if not group:
            return []
        tg_ids = eval(group.tg_ids)
        stmt = select(Chat).where(Chat.user_id.in_(tg_ids)).order_by(
            Chat.id.desc()).limit(limit).offset(offset)
        result = await session.execute(stmt)
        chats = result.scalars().all()
        messages = []
        for chat in chats:
            msg = await session.get(Message, chat.message_id)
            messages.append(msg)
        return messages
