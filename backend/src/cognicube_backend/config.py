from pydantic_settings import BaseSettings
from functools import lru_cache

class Setting(BaseSettings):
    """读取环境变量"""
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str = "smtp.qq.com"
    MAIL_PORT: int = 465
    MAIL_FROM: str
    USER_DB_URL: str = "sqlite:///./tests/databases/test_user.db"
    JWT_SECRET_KEY: str
    CON_DB_URL: str =  "sqlite:///./tests/databases/test_conversation.db"

    class Config:
        """读取配置文件"""
        env_file = ".env"

@lru_cache
def get_config():
    """返回设置对象，且保证只读取一次"""
    return Setting() # type: ignore

CONFIG = get_config()