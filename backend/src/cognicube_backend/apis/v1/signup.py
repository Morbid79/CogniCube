from fastapi import APIRouter, HTTPException
from src.cognicube_backend.models.user import User
from src.cognicube_backend.services.email_service import send_verification_email
from src.cognicube_backend.services.gsheet_service import add_user_to_sheet

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
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") from e
