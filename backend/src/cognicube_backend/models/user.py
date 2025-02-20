from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from cognicube_backend.databases.user_database import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """数据库中的User模型"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, index=True)
    verification_token_expiry = Column(DateTime(timezone=True))
    created_on = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    @property
    def password(self):
        """密码属性不可读"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

# 用户表相关操作
def get_user(db: Session, user_id: int):
    """查询并获取用户"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, email: str,
                password: str, verification_token: str,
                token_expiry: datetime
                ):
    """创建用户"""
    user = User(username=username, email=email,
                password=password,
                verification_token = verification_token,
                verification_token_expiry = token_expiry)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
