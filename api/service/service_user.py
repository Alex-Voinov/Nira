from database.models.User import User
from database.models.Goal import Goal
from api.schemas.schemas_user import UserBase


async def service_create_user(data: UserBase):

<<<<<<< HEAD
    # Создаем нового пользователя через Base.create
    user = await User.create(
        **data
    )
=======
    # Создаем цели
    for el in data.goal:
        await Goal.create(user_id=data.tg_id, goal=el)
    
    # Создаем пользователя
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
        photo_url=data.photo_url,
        description=data.description
    )

    print(user)
    return {"status": 200, "message": "пользователь успешно создан"}

async def service_receive_user(user_id: int):
    user = await User.find_by("tg_id", user_id)
    goals_db = await Goal.find_by("user_id", user_id)
    goals: List[str] = [el.goal for el in goals_db]
    
    return {
        "tg_id": user.tg_id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "show_gender": user.show_gender,
        "city": user.city,
        "current_country": user.current_country,
        "height": user.height,
        "weight": user.weight,
        "goal": goals,
        "photo_url": user.photo_url,
        "count_photo": user.count_photo
        "description": user.description
    }