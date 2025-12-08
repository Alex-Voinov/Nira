from pydantic import BaseModel
from typing import Optional

class DislikeBase(BaseModel):
    user_id: int
    target_id: int

    class Config:
        from_attributes = True  # ← это важно для FastAPI + SQLAlchemy