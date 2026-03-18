from fastapi import FastAPI
from src.api.routers.translate_router import router as translate_router


def init_routers(app_: FastAPI) -> None:
    app_.include_router(translate_router)

