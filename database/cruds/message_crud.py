from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session
from .models import User, Photo, Message, Chat, Group, Like, Dislike


async def create_message(sender_id: int, target_id: int, text: str, attachments=None):
    """Создать сообщение и связь с чатом"""
    async with async_session() as session:
        async with session.begin():
            message = Message(sender_id=sender_id, text=text,
                              attachments=attachments)
            session.add(message)
            await session.flush()  # чтобы получить id
            chat_entry = Chat(user_id=sender_id,
                              target_id=target_id, message_id=message.id)
            session.add(chat_entry)
            await session.commit()
            return message


async def update_message_by_id(message_id: int, editor_id: int, new_text: str):
    """Обновить сообщение"""
    async with async_session() as session:
        async with session.begin():
            message = await session.get(Message, message_id)
            if not message or message.sender_id != editor_id:
                return None
            message.text = new_text
            message.edited_at = func.now()
            await session.commit()
            return message


async def delete_message_by_id(message_id: int, requester_id: int):
    """Удалить сообщение и чат entry"""
    async with async_session() as session:
        async with session.begin():
            message = await session.get(Message, message_id)
            if not message or message.sender_id != requester_id:
                return {"success": False}
            chat_entries = await session.execute(select(Chat).where(Chat.message_id == message_id))
            for c in chat_entries.scalars():
                await session.delete(c)
            await session.delete(message)
            await session.commit()
            return {"success": True}
