from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, BigInteger, Text
from ..base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(Text)
    show_gender: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(Text)
    current_country: Mapped[str] = mapped_column(Text)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)
    goal: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(String(256))
