import uvicorn

from src.cognicube_backend import APP

uvicorn.run(APP, host="127.0.0.1", port=8000)