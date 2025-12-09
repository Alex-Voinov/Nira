from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    tg_id: int
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    show_gender: Optional[str] = None
    city: Optional[str] = None
    current_country: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
<<<<<<< HEAD
    goal: Optional[str] = None
=======
    goal: Optional[List[str]] = []
>>>>>>> 58c8d1a (добавил модель бд goal и связку с user.добавил get запрос на пользователя.поправил получения метчей и удалил импортирующиеся файл которые не сипользуются.)
    description: Optional[str] = None

    class Config:
        from_attributes = True