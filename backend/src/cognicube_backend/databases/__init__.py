from .user_database import init_db as init_user_db
from .conversation_database import init_db as init_conversation_db

def init_db():
    """初始化数据库"""
    init_user_db()
    init_conversation_db()
