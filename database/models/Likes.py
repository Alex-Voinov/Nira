import time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer
from database.base import Base 
class Likes(Base):
    __tablename__ = "likes"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    target_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    liked_at: Mapped[int] = mapped_column(Integer, nullable=False, default=lambda: int(time.time()))
