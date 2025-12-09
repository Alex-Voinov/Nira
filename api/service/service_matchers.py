from database.cruds.likes import add_like
from database.models.Likes import Likes
from database.models.Matchers import Matchers
from database.models.User import User
from database.models.Goal import Goal
from typing import Dict, List


async def service_receive_likes(user_id: int):
    return await Likes.find_by("user_id", user_id)


async def service_receive_matchers(user_id: int):
    # Ищем матчи, где user_id = one_user_id
    matches = await Matchers.find_by("one_user_id", user_id)

    if matches:
        target_user_id = matches[0].two_user_id
        user = await User.find_by("tg_id", target_user_id)
        goals_db = await Goal.find_by("user_id", target_user_id)
        
        goals: List[str] = [el.goal for el in goals_db]  # формируем массив целей

        return {
            "tg_id": user.tg_id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "show_gender": user.show_gender,
            "city": user.city,
            "current_country": user.current_country,
            "height": user.height,
            "weight": user.weight,
            "goal": goals,
            "description": user.description
        }

    # Ищем матчи, где user_id = two_user_id
    matches = await Matchers.find_by("two_user_id", user_id)
    if matches:
        target_user_id = matches[0].one_user_id
        user = await User.find_by("tg_id", target_user_id)
        goals_db = await Goal.find_by("user_id", target_user_id)
        goals: List[str] = [el.goal for el in goals_db]

        return {
            "tg_id": user.tg_id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "show_gender": user.show_gender,
            "city": user.city,
            "current_country": user.current_country,
            "height": user.height,
            "weight": user.weight,
            "goal": goals,
            "description": user.description
        }

    return []  # если матчей нет


async def service_add_like(user_id: int, target_id: int) -> Dict:
    # Валидация входных данных
    if not isinstance(user_id, int) or not isinstance(target_id, int):
        raise ValueError("user_id и target_id должны быть int")
    if user_id <= 0 or target_id <= 0:
        raise ValueError("ID пользователей должны быть положительными числами")

    # Логика обработки лайка
    result = await add_like(user_id, target_id)

    if result.get("liked") is False and result.get("reason"):
        raise ValueError(result["reason"])

    return {"status": 200, "message": "лайк успешно поставлен"}
