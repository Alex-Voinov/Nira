from fastapi import APIRouter, HTTPException
from api.service.service_like import service_receive_likes
from api.schemas.schemas_like import LikeBase

router = APIRouter()


@router.get("/likes/{user_id}")
async def get_likes(
    user_id: int,
):
    """Получение входящих лайков пользователя"""
    likes = await service_receive_likes(user_id)

    if not likes:
        raise HTTPException(status_code=404, detail="Лайки не найдены")

    return likes
