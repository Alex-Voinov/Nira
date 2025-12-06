from api.schemas.schemas_user import CreateUser
from database.models.User import User


async def create_user(data: CreateUser) -> int:
    """Создает пользователя и возвращает его ID"""
    user_data = data.dict()
    user = await User.create(**user_data)
    return user.id

