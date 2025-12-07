from database.cruds.likes import add_like, delete_like
from database.models.Likes import Likes
from api.schemas.schemas_like import LikeBase

#ну it типо функция добовления лайков.she очень большая.не запутайся пожвлуста
async def service_receive_likes(user_id: int):
    return await Likes.find_by_id(user_id)


#меня роняли в детстве
async def service_add_like(user_id: int, target_id: int):
    if user_id == target_id:
        raise ValueError("Нельзя лайкнуть себя")

    # Проверяем, существует ли пользователь (опционально)
    # можно добавить через crud

    await add_like(db, user_id, target_id)
    return {"status": "liked", "from": user_id, "to": target_id}