from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Integer, Text
from database.base import Base

class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(Text)
    show_gender: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(Text)
    current_country: Mapped[str] = mapped_column(Text)
    height: Mapped[int] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer)

    photo_url: Mapped[str] = mapped_column(Text)
    count_photo: Mapped[int] = mapped_column(Integer)

    description: Mapped[str] = mapped_column(String(256))