from pydantic import SecretStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

# 邮件服务器配置
mail_config = ConnectionConfig(
    MAIL_USERNAME="cognicubeorg@gmail.com",
    MAIL_PASSWORD=SecretStr("ayau ktnx vpiy nigb"),
    MAIL_FROM="cognicubeorg@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="CogniCube Team",
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,  # 添加这行
    MAIL_SSL_TLS=False  # 添加这行
)

async def send_verification_email(email: str):
    """发送电子邮件验证码"""
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body="Thank you for registering. Please verify your email.",
        subtype=MessageType.html
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
    print(f"Verification email sent to {email}.")
