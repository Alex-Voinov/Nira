from database.cruds.likes import add_like, delete_like
from database.models.Likes import Likes
from api.schemas.schemas_like import LikeBase
from typing import Dict

# ну it типо функция добовления лайков.she очень большая.не запутайся пожвлуста


async def service_receive_likes(user_id: int):
    return await Likes.find_by("user_id", user_id)


async def service_add_like(user_id: int, target_id: int) -> Dict:
    # Валидация входных данных
    if not isinstance(user_id, int) or not isinstance(target_id, int):
        raise ValueError("user_id и target_id должны быть int")
    if user_id <= 0 or target_id <= 0:
        raise ValueError("ID пользователей должны быть положительными числами")
    # Логика обработки лайка
    result = await add_like(user_id, target_id)
    # Если crud вернул reason — считаем это клиентской ошибкой
    if result.get("liked") is False and result.get("reason"):
        raise ValueError(result["reason"])
    # Успешно
    return {"status": 200, "message": "лайк успешно поставлен"}
