# database/models/Message.py
from sqlalchemy import Column, BigInteger, DateTime, Text, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from ..base import Base


class Message(Base):
    __tablename__ = "messages"

    chat_id = Column(BigInteger, ForeignKey("chats.id"), nullable=False)        # ← теперь ссылаемся на id!
    sender_id = Column(BigInteger, ForeignKey("users.tg_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    text = Column(Text, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('chat_id', 'sender_id', 'created_at'),
    )