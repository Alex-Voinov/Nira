from pydantic import BaseModel

class DislikeBase(BaseModel):
    user_id: int
    target_id: int

    class Config:
        from_attributes = True  # ← это важно для FastAPI + SQLAlchemy