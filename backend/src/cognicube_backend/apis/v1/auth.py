from fastapi import APIRouter

router = APIRouter(prefix="/apis/v1/auth")


@router.get("/")
async def read_root():
    return {"Hello": "World"}