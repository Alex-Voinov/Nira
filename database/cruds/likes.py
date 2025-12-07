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


async def add_like(user_id: int, target_id: int):
    """Добавить лайк и при взаимном лайке создать матч"""
    if user_id == target_id:
        return {"liked": False, "reason": "cannot_like_self"}
    async with async_session() as session:
        async with session.begin():
            existing = await session.execute(select(Like).where(Like.user_id == user_id, Like.target_id == target_id))
            if existing.scalar_one_or_none():
                return {"liked": False, "reason": "already_liked"}
            like = Like(user_id=user_id, target_id=target_id)
            session.add(like)
            # Проверить взаимный лайк
            rev = await session.execute(select(Like).where(Like.user_id == target_id, Like.target_id == user_id))
            if rev.scalar_one_or_none():
                # Создать match
                a, b = sorted([user_id, target_id])
                match = Match(one_user_id=a, two_user_id=b)
                session.add(match)
                await session.commit()
                return {"liked": True, "new_match": match}
            await session.commit()
            return {"liked": True}


async def delete_like(user_id: int, target_id: int):
    """Удалить лайк"""
    async with async_session() as session:
        async with session.begin():
            like = await session.execute(select(Like).where(Like.user_id == user_id, Like.target_id == target_id))
            like_obj = like.scalar_one_or_none()
            if not like_obj:
                return {"success": False}
            await session.delete(like_obj)
            # Удалить match если есть
            a, b = sorted([user_id, target_id])
            match = await session.execute(select(Match).where(Match.one_user_id == a, Match.two_user_id == b))
            match_obj = match.scalar_one_or_none()
            if match_obj:
                await session.delete(match_obj)
            await session.commit()
            return {"success": True}
