"""
@Description :   实现对用户数据库模型的链接与操作
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from datetime import datetime

from cognicube_backend.models.user import User
from .. import CONFIG


USER_DB_PATH = CONFIG.USER_DB_PATH
SQLALCHEMY_DATABASE_URL = f"sqlite:///{USER_DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """为当前对话获取数据库"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 用户表相关操作
def get_user(db: Session, user_id: int):
    """查询并获取用户"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, email: str,
                password_hash: str, verification_token: str,
                token_expiry: datetime
                ):
    """创建用户"""
    user = User(username=username, email=email, 
                password_hash=password_hash,
                verification_token = verification_token,
                verification_token_expiry = token_expiry)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
