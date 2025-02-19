from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from cognicube_backend.models.user import UserCreate, UserInDB
from cognicube_backend.services.email_service import send_verification_email
from cognicube_backend.services.gsheet_service import add_user_to_sheet
from cognicube_backend.databases.user_database import create_user
from cognicube_backend.databases import SessionLocal

router = APIRouter()

@router.post("/register/")
async def signup_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    try:
        # 创建用户
        user_in_db = create_user(db, user)

        # 将用户邮箱写入 Google Sheet
        add_user_to_sheet(user.email)

        # 发送验证邮件
        await send_verification_email(user.email)

        return {"user_id": str(user_in_db.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e
