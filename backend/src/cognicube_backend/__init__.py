from fastapi import FastAPI
from .apis.v1.auth import router

APP = FastAPI()

@APP.get("/")
async def root():
    return {"message": "please don't use this endpoint"}

APP.include_router(router)
