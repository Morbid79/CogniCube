from jinja2 import Environment, FileSystemLoader
from pydantic import SecretStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from .. import CONFIG

# 配置模板环境
template_env = Environment(loader=FileSystemLoader("./templates/auth/email"))  # 模板文件所在的目录

# 邮件服务器配置
mail_config = ConnectionConfig(
    MAIL_USERNAME=CONFIG.MAIL_USERNAME,
    MAIL_PASSWORD=SecretStr(CONFIG.MAIL_PASSWORD),
    MAIL_FROM=CONFIG.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME=CONFIG.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=True,  # 添加这行
    MAIL_SSL_TLS=False  # 添加这行
)

async def send_verification_email(email: str, username: str,
                                  verification_token: str):
    """发送电子邮件验证码"""
    # 加载模板
    template = template_env.get_template("confirm.txt")
    body = template.render(username = username, token = verification_token)
    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
    print(f"Verification email sent to {email}.")
