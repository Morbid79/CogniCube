from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from cognicube_backend.schemas.user import UserLogin
from cognicube_backend.databases.user_database import  get_db
from cognicube_backend.models.user import User
from cognicube_backend.schemas.user import TokenResponse
from cognicube_backend.utils.jwt import create_jwt_token

auth = APIRouter(prefix="/apis/v1/auth")


@auth.get("/")
async def read_root():
    return "please don't use this endpoint"

@auth.post("/login",response_model=TokenResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_db.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")
    
    # 生成访问令牌
    access_token = create_jwt_token(
        {"sub": user.username, "type": "access"},
        timedelta(days=1)
    )
    
    return {
        "user_id": user_db.id,
        "access_token": access_token,
    }
 