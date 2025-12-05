from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, BigInteger, Text
from ..base import Base


class Message(Base):
    __tablename__ = "messages"

    sender_id: Mapped[int] = mapped_column(BigInteger)
    text: Mapped[str] = mapped_column(Text)
    attachments: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    edited_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)