from fastapi import FastAPI
from src.cognicube_backend.apis.v1.auth import router
from . import config

APP = FastAPI()
CONFIG = config.get_config()

@APP.get("/")
async def root():
    return {"message": "please don't use this endpoint"}

APP.include_router(router)
