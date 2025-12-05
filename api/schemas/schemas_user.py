from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    tg_id: int
    name: str
    age: int
    gender: Optional[str] = None
    show_gender: Optional[str] = None
    city: Optional[str] = None
    current_country: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    goal: Optional[str] = None
    description: Optional[str] = None