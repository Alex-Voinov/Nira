# database/models/Chat.py
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # ← ЭТО ОБЯЗАТЕЛЬНО!

    user1_id = Column(BigInteger, ForeignKey("users.tg_id"), nullable=False, index=True)
    user2_id = Column(BigInteger, ForeignKey("users.tg_id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Чтобы не было дублей чатов (опционально, но очень желательно)
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='unique_chat_pair'),
    )