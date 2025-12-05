from api.schemas.schemas_user import CreateUser
from database.models.User import User


async def create_user(data: CreateUser):
    user_data = data.dict()
    user = await User.create(**user_data)
    return {"status": 200, "message": "Пользователь успешно создан", "user_id": user.id}

