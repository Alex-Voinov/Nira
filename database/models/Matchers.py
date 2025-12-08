import time
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer
from database.base import Base

class Matchers(Base):
    __tablename__ = "matchers"

    one_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    two_user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    matched_at: Mapped[int] = mapped_column(Integer, nullable=False, default=lambda: int(time.time()))
