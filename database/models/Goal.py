from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, Integer
import time
from database.base import Base 

class Goal(Base):
    __tablename__ = "goal"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    matched_at: Mapped[int] = mapped_column(Integer, nullable=False, default=lambda: int(time.time()))
