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
    goal: Optional[List[str]] = []
    description: Optional[str] = None

    class Config:
        from_attributes = True