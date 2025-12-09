from fastapi import APIRouter, HTTPException
from api.service.service_like import service_receive_likes
from api.service.service_matchers import service_receive_matchers

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

@router.get("/matchers/{user_id}")
async def get_likes(
    user_id: int,
):
    """Получение входящих метчей пользователя"""
    matchers = await service_receive_matchers(user_id)

    if not matchers:
        raise HTTPException(status_code=404, detail="Метчей не найдены")

    return matchers