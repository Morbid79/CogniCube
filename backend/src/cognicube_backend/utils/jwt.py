from datetime import datetime, timedelta, timezone
from jose import jwt

from cognicube_backend.config import CONFIG
def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    """生成JWT令牌"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, CONFIG.JWT_SECRET_KEY, algorithm="HS256")