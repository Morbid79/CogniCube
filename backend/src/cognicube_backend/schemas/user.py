"""
@Description :   用户的Pydantic 模型（用于请求/响应）
"""
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_on: datetime
    is_verified: bool

    class Config:
        from_attributes = True
