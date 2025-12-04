from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, BigInteger, Text
from ..base import Base


class Views(Base):
    __tablename__ = "views"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    target_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    views_at: Mapped[int] = mapped_column(Integer)