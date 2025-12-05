from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from .db import async_session
from .models import User, Photo, Message, Chat, Group, Like, Dislike

async def get_user_by_tg_id(tg_id: int):
    """Получить пользователя по tg_id"""
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user  # если нет — None

async def update_user_by_tg_id(tg_id: int, patch: dict):
    """Обновить пользователя по tg_id"""
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.tg_id == tg_id).with_for_update()
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if not user:
                return None
            for key, value in patch.items():
                setattr(user, key, value)
            await session.commit()
            return user

async def delete_user_by_tg_id(tg_id: int, soft_delete=True):
    """Удалить пользователя по tg_id"""
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, tg_id)
            if not user:
                return {"success": False}
            if soft_delete:
                user.deleted_at = func.now()
            else:
                # Hard delete: удалить все связи
                await session.execute(delete(Photo).where(Photo.user_tg_id == tg_id))
                await session.execute(delete(Like).where((Like.user_id == tg_id) | (Like.target_id == tg_id)))
                await session.execute(delete(Dislike).where((Dislike.user_id == tg_id) | (Dislike.target_id == tg_id)))
                await session.execute(delete(Chat).where((Chat.user_id == tg_id) | (Chat.target_id == tg_id)))
                await session.execute(delete(Message).where(Message.sender_id == tg_id))
                await session.delete(user)
            await session.commit()
            return {"success": True}