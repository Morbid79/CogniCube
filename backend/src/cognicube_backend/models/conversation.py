from datetime import datetime, UTC
from enum import Enum
from sqlalchemy import  Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from cognicube_backend.databases.user_database import Base

class Who(Enum):
    USER = "User"
    AI = "AI"

class Conversation(Base):
    """数据库中的聊天记录模型"""
    __tablename__ = "Conversations"
    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    message: Mapped[str] = mapped_column(String)
    who: Mapped[Who] = mapped_column(String)
    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))