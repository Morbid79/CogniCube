from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# 邮件服务器配置
mail_config = ConnectionConfig(
    MAIL_USERNAME="cognicubeorg@gmail.com",
    MAIL_PASSWORD="ayau ktnx vpiy nigb",
    MAIL_FROM="cognicubeorg@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="CogniCube Team",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

async def send_verification_email(email: str):
    """发送电子邮件验证码"""
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body="Thank you for registering. Please verify your email.",
        subtype="html"
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
    print(f"Verification email sent to {email}.")
