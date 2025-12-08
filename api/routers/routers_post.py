from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_session

from api.schemas.schemas_like import LikeBase
from api.schemas.schemas_dislike import DislikeBase
from api.schemas.schemas_user import UserBase
from api.service.service_like import service_add_like
from api.service.service_dislike import service_add_dislike
from api.service.service_user import service_create_user

router = APIRouter()

# тут прописана логика кода сделана Доценко Егором Дмитриевичем


@router.post("/registration")
async def create_user_endpoint(user: UserBase):
    """
    Создание нового пользователя.
    Логика находится в service/user.py
    """
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Имя не может быть пустым")
    if user.age <= 0:
        raise HTTPException(
            status_code=400, detail="Возраст должен быть положительным")
    try:
        return await service_create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/like")
async def add_like_endpoint(data: LikeBase):
    try:
        return await service_add_like(data.user_id, data.target_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/dislike")
async def add_dislike_endpoint(data: DislikeBase):
    try:
        return await service_add_dislike(data.user_id, data.target_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера")
