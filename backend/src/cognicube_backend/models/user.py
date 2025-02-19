from sqlalchemy import Column, Integer, String, Boolean, DateTime
from cognicube_backend.databases.user_database import Base
from datetime import datetime, UTC

class User(Base):
    """数据库中的User模型"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, index=True)
    verification_token_expiry = Column(DateTime)
    created_on = Column(DateTime, default=datetime.now(UTC))
