from fastapi import APIRouter, HTTPException, status
from api.schemas.schemas_user import CreateUser
from api.service.user import create_user

router = APIRouter()

# короче я хотел сделать, как в node, чтобы были controller, service,
# но я так понял будет слишком много не нужного кода,
# по этому controller не будет.будет только srvice.логику
# из нее сюда буду передовать


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def post_create_user(user: CreateUser):
    """Создание нового пользователя"""
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Имя не может быть пустым")
    if user.age <= 0:
        raise HTTPException(
            status_code=400, detail="Возраст должен быть положительным"
        )
    try:
        user_id = await create_user(user)
        return {"message": "Пользователь успешно создан", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
