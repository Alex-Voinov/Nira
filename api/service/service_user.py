from database.cruds.users import get_user_by_tg_id, update_user_by_tg_id
from database.models.User import User
from api.schemas.schemas_user import UserBase


async def service_create_user(data: UserBase):

    # Создаем нового пользователя через Base.create
    user = await User.create(
        tg_id=data.tg_id,
        name=data.name,
        age=data.age,
        gender=data.gender,
        show_gender=data.show_gender,
        city=data.city,
        current_country=data.current_country,
        height=data.height,
        weight=data.weight,
        goal=data.goal,
        description=data.description
    )
    print(user)
    return {"status": 200, "message": "пользователь успешно создан"}
