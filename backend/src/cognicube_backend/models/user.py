from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional
from datetime import datetime
import re

# 密码正则表达式    # 至少6位，包含字母和数字
password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'

# 用户注册请求模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="User's unique username")
    password: str = Field(..., min_length=6, description="User password (hashed later)")
    email: EmailStr = Field(..., description="User's email address")

# 数据库中的用户模型（带ID和时间戳）
class UserInDB(UserCreate):
    id: int = Field(..., description="Unique user ID")
    created_at: datetime = Field(default_factory=datetime.datetime.utcnow, description="User creation timestamp")
    email_verified: bool = Field(default=False, description="Email verification status")

    class Config:
        orm_mode = True

# 仅用于邮箱验证的模型
class UserEmail(BaseModel):
    email: EmailStr = Field(..., description="User email for verification purposes")

