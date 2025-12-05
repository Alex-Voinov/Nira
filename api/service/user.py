from api.schemas.schemas_user import CreateUser
from database.models.User import User
from sqlalchemy.exc import IntegrityError


async def create_user(data: CreateUser):

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
