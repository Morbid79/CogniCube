from fastapi import FastAPI

from . import config

from cognicube_backend.apis.v1.auth import router


APP = FastAPI()
CONFIG = config.get_config()

@APP.get("/")
async def root():
    return {"message": "please don't use this endpoint"}

APP.include_router(router)
