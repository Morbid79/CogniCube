from pydantic import BaseModel, Field
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class UserBase(BaseModel):
    username: str = Field(..., description="User id")
    password: str = Field(..., description="User password")
    email: str = Field(..., description="User email")
    created_at: str = Field(..., description="User creation date")
    email_verified: bool = Field(False, description="Email verification status")

class User(UserBase):
    id: int = Field(..., description="User id")

    class Config:
        orm_mode = True

def send_verification_email(email: str):
    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = email
    msg['Subject'] = 'Verify your email'

    # 验证链接
    verification_link = 'http://yourdomain.com/verify?email=' + email

    # 邮件正文
    body = 'Please click on the following link to verify your email: ' + verification_link
    msg.attach(MIMEText(body, 'plain'))

    # 发送邮件
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('your_email@example.com', 'your_password')
    text = msg.as_string()
    server.sendmail('your_email@example.com', email, text)
    server.quit()

def register_user(username: str, password: str, email: str):
    # 创建用户
    user = User(username=username, password=password, email=email, email_verified=False)

    # 发送验证邮件
    send_verification_email(email)

    # 返回用户
    return user
