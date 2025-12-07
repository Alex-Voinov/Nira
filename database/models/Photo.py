from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, BigInteger
from database.base import Base

class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    user_tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_profile: Mapped[bool] = mapped_column(Boolean, default=False)