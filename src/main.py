import uvicorn
from async_generator import asynccontextmanager
from fastapi import FastAPI
import sys
import logging
from pathlib import Path

from src.api.routers.routers import init_routers
from src.setup import redis_connector


sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    yield
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)

init_routers(app_=app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
