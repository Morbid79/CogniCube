from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import uuid
from datetime import datetime, timedelta, UTC

from cognicube_backend.schemas.user import UserCreate
from cognicube_backend.services.email_service import send_verification_email
from cognicube_backend.services.gsheet_service import add_user_to_sheet
from cognicube_backend.databases.user_database import User, create_user, SessionLocal

router = APIRouter()

@router.post("/register")
async def signup_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    # 确保用户名和邮箱的唯一性
    db_user = db.query(User).filter((User.username == user.username) |
                                    (User.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")

    try:
        # 生成用户验证token，并在5分钟后过期
        verfication_token = str(uuid.uuid4())
        token_expiry = datetime.now(UTC) + timedelta(minutes=5)

        # 创建用户
        user_in_db = create_user(db, user.username, user.email,
                                 user.password_hash,
                                 verfication_token,
                                 token_expiry)

        # 将用户邮箱写入 Google Sheet
        # add_user_to_sheet(user.email)

        # 发送验证邮件
        await send_verification_email(user.email, user.username,
                                      verfication_token)

        return {"user_id": str(user_in_db.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e

@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(SessionLocal)):
    """根据token对邮箱进行验证"""
    db_user = db.query(User).filter(User.verification_token == token).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    # 检查是否已经过期
    if db_user.verification_token_expiry < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Verification token has expired")

    # 邮箱已验证
    db_user.is_verified = True
    db_user.verification_token = None  # 将token移除
    db_user.verification_token_expiry = None  # 将token过期时间移除
    db.add(db_user)
    db.commit()

    return {"message": "Email verified successfully", "username": db_user.username}
