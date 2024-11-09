from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from .endpoints import router as api_router


def get_fastapi():
    _api = FastAPI()

    _api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _api


api = get_fastapi()


@api.get("/")
def get():
    return {"message": "Hello World!"}


api.include_router(api_router)
