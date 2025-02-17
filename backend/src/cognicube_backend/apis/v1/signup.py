from fastapi import APIRouter, HTTPException
from models.user import User
from services.email_service import send_verification_email
from services.gsheet_service import add_user_to_sheet

router = APIRouter()

@router.post("/register/")
async def register_user(user: User):
    try:
        # 将用户邮箱写入Google Sheet
        add_user_to_sheet(user.email)

        # 发送验证邮件
        await send_verification_email(user.email)

        return {"message": "Verification email sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")
