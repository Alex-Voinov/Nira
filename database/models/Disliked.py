import time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer
from database.base import Base

class Disliked(Base):
    __tablename__ = "disliked"
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    target_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    disliked_at: Mapped[int] = mapped_column(Integer, nullable=False, default=lambda: int(time.time()))
