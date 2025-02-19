from pydantic_settings import BaseSettings
from functools import lru_cache

class Setting(BaseSettings):
    """读取环境变量"""
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    USER_DB_PATH: str = "./databases/test_user.db"

    class Config:
        """读取配置文件"""
        env_file = ".env"

@lru_cache
def get_config():
    """返回设置对象，且保证只读取一次"""
    return Setting()
