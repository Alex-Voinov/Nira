from sqlalchemy import select, update, delete, func
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


async def add_photo(user_tg_id: int, url: str, is_profile=False):
    """Добавить фото"""
    async with async_session() as session:
        async with session.begin():
            if is_profile:
                # Сделать все фото пользователя не профильными
                await session.execute(
                    update(Photo)
                    .where(Photo.user_tg_id == user_tg_id)
                    .values(is_profile=False)
                )
            photo = Photo(user_tg_id=user_tg_id,
                          url=url, is_profile=is_profile)
            session.add(photo)
            await session.commit()
            return photo


async def get_photos_by_tg_id(user_tg_id: int):
    """Получить фото пользователя"""
    async with async_session() as session:
        stmt = select(Photo).where(Photo.user_tg_id == user_tg_id).order_by(
            Photo.is_profile.desc(), Photo.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()


async def update_photo_by_id(photo_id: int, patch: dict):
    """Обновить фото"""
    async with async_session() as session:
        async with session.begin():
            photo = await session.get(Photo, photo_id)
            if not photo:
                return None
            for key, value in patch.items():
                setattr(photo, key, value)
            await session.commit()
            return photo


async def delete_photo_by_id(photo_id: int):
    """Удалить фото"""
    async with async_session() as session:
        async with session.begin():
            photo = await session.get(Photo, photo_id)
            if not photo:
                return {"success": False}
            await session.delete(photo)
            await session.commit()
            return {"success": True}
