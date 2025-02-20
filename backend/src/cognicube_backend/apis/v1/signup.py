import uuid
from datetime import datetime, timedelta, UTC
import traceback

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import pytz

from cognicube_backend.schemas.user import UserCreate
from cognicube_backend.services.email_service import send_verification_email
from cognicube_backend.services.gsheet_service import add_user_to_sheet
from cognicube_backend.databases.user_database import  get_db
from cognicube_backend.models.user import User, create_user

signup = APIRouter(prefix="/apis/v1/signup")

@signup.post("/register")
async def signup_user(request:Request,
                      user: UserCreate, db: Session = Depends(get_db)):
    # 确保用户名和邮箱的唯一性
    db_user = db.query(User).filter((User.username == user.username) |
                                    (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Username or Email already registered")

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
        await send_verification_email(request, user.email,
                                      verfication_token)

        return {"user_id": str(user_in_db.id)}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e

@signup.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """根据token对邮箱进行验证"""
    db_user = db.query(User).filter(User.verification_token == token).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")

    token_expiry_with_tz = db_user.verification_token_expiry.replace(tzinfo=pytz.UTC)

    # 检查是否已经过期
    if token_expiry_with_tz < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Verification token has expired")

    # 邮箱已验证
    db_user.is_verified = True
    db_user.verification_token = None  # 将token移除
    db_user.verification_token_expiry = None  # 将token过期时间移除
    db.add(db_user)
    db.commit()

    return {"message": "Email verified successfully", "username": db_user.username}
