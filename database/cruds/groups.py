import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import async_session
from ..models.User import User
from ..models.Photo import Photo
from ..models.Message import Message
from ..models.Chat import Chat
from ..models.Group import Group
from ..models.Likes import Likes
from ..models.Disliked import Disliked
from ..models.Views import Views
from ..models.Matchers import Matchers

async def create_group(name: str, tg_ids: list[int]):
    """Создать группу"""
    async with async_session() as session:
        async with session.begin():
            # храним как JSON
            group = Group(name=name, tg_ids=json.dumps(tg_ids))
            session.add(group)
            return group


async def get_group_messages(group_id: int, limit=50, offset=0):
    """Получить сообщения группы"""
    async with async_session() as session:
        group = await session.get(Group, group_id)
        if not group:
            return []

        tg_ids = json.loads(group.tg_ids)
        stmt = select(Chat).where(Chat.user_id.in_(tg_ids)).order_by(
            Chat.id.desc()
        ).limit(limit).offset(offset)

        result = await session.execute(stmt)
        chats = result.scalars().all()

        # Получаем все сообщения одной выборкой
        message_ids = [chat.message_id for chat in chats]
        if not message_ids:
            return []

        msg_stmt = select(Message).where(Message.id.in_(message_ids))
        msg_result = await session.execute(msg_stmt)
        messages = msg_result.scalars().all()

        # Можно вернуть сообщения в порядке чата
        messages.sort(key=lambda m: message_ids.index(m.id))
        return messages
