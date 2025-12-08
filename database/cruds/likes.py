# database/cruds/likes.py
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from ..db import async_session
from ..models.Likes import Likes
from ..models.Matchers import Matchers

async def add_like(user_id: int, target_id: int) -> dict:
    """
    Добавить лайк. Если взаимный — создать матч (Matchers).
    Возвращает dict с ключами:
      - liked: bool
      - reason: str (опционально)
      - new_match: Matchers (опционально, объект SQLAlchemy)
    """
    if user_id == target_id:
        return {"liked": False, "reason": "cannot_like_self"}

    # Чтобы упорядочивать id для матча: всегда меньший — first
    a, b = sorted([user_id, target_id])

    async with async_session() as session:
        async with session.begin():
            # Проверяем уже ли есть лайк от user -> target
            existing = await session.execute(
                select(Likes).where(Likes.user_id == user_id, Likes.target_id == target_id)
            )
            if existing.scalar_one_or_none():
                return {"liked": False, "reason": "already_liked"}

            # Создаём лайк
            like = Likes(user_id=user_id, target_id=target_id)
            session.add(like)

            # Проверяем обратный лайк (target -> user)
            rev = await session.execute(
                select(Likes).where(Likes.user_id == target_id, Likes.target_id == user_id)
            )
            if rev.scalar_one_or_none():
                # если матча ещё нет — создаём
                match_sel = await session.execute(
                    select(Matchers).where(Matchers.one_user_id == a, Matchers.two_user_id == b)
                )
                if not match_sel.scalar_one_or_none():
                    match = Matchers(one_user_id=a, two_user_id=b)
                    session.add(match)
                    # Не вызываем session.commit() вручную — session.begin() сделает это.
                    return {"liked": True, "new_match": match}
                else:
                    # match уже есть (редкий кейс)
                    return {"liked": True, "new_match": None}
            # нет взаимного лайка
            return {"liked": True}

async def delete_like(user_id: int, target_id: int) -> dict:
    """
    Удалить лайк. Если после удаления матча больше нет (нестоит взаимного лайка) — удалить Matchers.
    Возвращает {"success": True/False}
    """
    if user_id == target_id:
        return {"success": False, "reason": "cannot_unlike_self"}

    a, b = sorted([user_id, target_id])

    async with async_session() as session:
        async with session.begin():
            like_sel = await session.execute(
                select(Likes).where(Likes.user_id == user_id, Likes.target_id == target_id)
            )
            like_obj = like_sel.scalar_one_or_none()
            if not like_obj:
                return {"success": False, "reason": "not_found"}

            # удаляем лайк
            await session.delete(like_obj)

            # Если до этого был матч (т.е. существовал обратный лайк), то
            # после удаления этого лайка нужнло проверить — остался ли обратный лайк.
            rev_sel = await session.execute(
                select(Likes).where(Likes.user_id == target_id, Likes.target_id == user_id)
            )
            rev_obj = rev_sel.scalar_one_or_none()
            if not rev_obj:
                # если обратного лайка нет — удалить матч (если он есть)
                match_sel = await session.execute(
                    select(Matchers).where(Matchers.one_user_id == a, Matchers.two_user_id == b)
                )
                match_obj = match_sel.scalar_one_or_none()
                if match_obj:
                    await session.delete(match_obj)

            return {"success": True}
