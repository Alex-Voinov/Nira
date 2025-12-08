from pydantic import BaseModel, validator

class LikeBase(BaseModel):
    user_id: int
    target_id: int

    @validator("user_id", "target_id")
    def positive_ids(cls, v):
        if v <= 0:
            raise ValueError("ID должно быть положительным")
        return v

    class Config:
        from_attributes = True
