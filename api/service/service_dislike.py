from database.cruds.dislikes import add_dislike, delete_dislike
from database.models.Disliked import Disliked
from api.schemas.schemas_dislike import DislikeBase


async def service_add_dislike(data: DislikeBase):
    await add_dislike(data.user_id, data.target_id)
    
    return {"status": 200, "message": "дизлайк успешно поставлен"}

