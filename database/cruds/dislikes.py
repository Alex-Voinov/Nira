from sqlalchemy import select
from ..db import async_session
from ..models.Disliked import Disliked
from ..models.Likes import Likes
from ..models.Matchers import Matchers

async def add_dislike(user_id: int, target_id: int):
    """Добавить дизлайк"""
    if user_id == target_id:
        return {"disliked": False, "reason": "cannot_dislike_self"}

    a, b = sorted([user_id, target_id])

    async with async_session() as session:
        async with session.begin():
            # удалить обратный лайк если есть
            rev_like = await session.execute(
                select(Likes).where(Likes.user_id == target_id, Likes.target_id == user_id)
            )
            rev_obj = rev_like.scalars().first()
            if rev_obj:
                await session.delete(rev_obj)

            # добавить дизлайк
            dislike = Disliked(user_id=user_id, target_id=target_id)
            session.add(dislike)

            # удалить матч если есть
            match_sel = await session.execute(
                select(Matchers).where(Matchers.one_user_id == a, Matchers.two_user_id == b)
            )
            match_obj = match_sel.scalars().first()
            if match_obj:
                await session.delete(match_obj)

    return {"disliked": True}


async def delete_dislike(user_id: int, target_id: int):
    """Удалить дизлайк"""
    async with async_session() as session:
        async with session.begin():
            dislike_sel = await session.execute(
                select(Disliked).where(Disliked.user_id == user_id, Disliked.target_id == target_id)
            )
            dislike_obj = dislike_sel.scalars().first()
            if not dislike_obj:
                return {"success": False}
            await session.delete(dislike_obj)

    return {"success": True}
