from database.cruds.users import get_user_by_tg_id, update_user_by_tg_id
from database.models.User import User
from api.schemas.schemas_user import UserBase


async def service_create_user(data: UserBase):

    # Создаем нового пользователя через Base.create
    user = await User.create(
        **data
    )
    print(user)
    return {"status": 200, "message": "пользователь успешно создан"}
