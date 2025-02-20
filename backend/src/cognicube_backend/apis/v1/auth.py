from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from cognicube_backend.schemas.user import UserLogin
from cognicube_backend.databases.user_database import  get_db
from cognicube_backend.models.user import User

auth = APIRouter(prefix="/apis/v1/auth")


@auth.get("/")
async def read_root():
    return {"Hello": "World"}

@auth.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_db.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Email or password incorrect")
    return {"user_id": user_db.id}
