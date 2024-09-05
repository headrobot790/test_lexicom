from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi import FastAPI

from src.config import settings
from src.router import phone_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
    yield
    await redis.close()

app = FastAPI(lifespan=lifespan)
app.include_router(phone_router)






