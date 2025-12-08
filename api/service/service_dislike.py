from database.cruds.dislikes import add_dislike, delete_dislike
from database.models.Disliked import Disliked
from api.schemas.schemas_dislike import DislikeBase


async def service_add_dislike(user_id: int, target_id: int):
    await add_dislike(user_id, target_id)

    return {"status": 200, "message": "дизлайк успешно поставлен"}
