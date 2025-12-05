from fastapi import APIRouter, HTTPException
from api.schemas.schemas_user import CreateUser
from api.service.user import create_user

router = APIRouter()

# короче я хотел сделать, как в node, чтобы были controller, service,
# но я так понял будет слишком много не нужного кода,
# по этому controller не будет.будет только srvice.логику
# из нее сюда буду передовать


@router.post("/create/user")
async def post_create_user(user: CreateUser):
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
        return await create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
