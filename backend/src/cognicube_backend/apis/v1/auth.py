from fastapi import APIRouter

auth = APIRouter(prefix="/apis/v1/auth")


@auth.get("/")
async def read_root():
    return {"Hello": "World"}