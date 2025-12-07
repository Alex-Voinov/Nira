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


async def add_dislike(user_id: int, target_id: int):
    """Добавить дизлайк"""
    async with async_session() as session:
        async with session.begin():
            # удалить обратный лайк если есть
            rev_like = await session.execute(select(Like).where(Like.user_id == target_id, Like.target_id == user_id))
            rev_obj = rev_like.scalar_one_or_none()
            if rev_obj:
                await session.delete(rev_obj)
            dislike = Dislike(user_id=user_id, target_id=target_id)
            session.add(dislike)
            # удалить match если есть
            a, b = sorted([user_id, target_id])
            match = await session.execute(select(Match).where(Match.one_user_id == a, Match.two_user_id == b))
            match_obj = match.scalar_one_or_none()
            if match_obj:
                await session.delete(match_obj)
            await session.commit()
            return {"disliked": True}


async def delete_dislike(user_id: int, target_id: int):
    """Удалить дизлайк"""
    async with async_session() as session:
        async with session.begin():
            dislike = await session.execute(select(Dislike).where(Dislike.user_id == user_id, Dislike.target_id == target_id))
            obj = dislike.scalar_one_or_none()
            if not obj:
                return {"success": False}
            await session.delete(obj)
            await session.commit()
            return {"success": True}
