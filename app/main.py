from app.database import Base
from app.database import engine
from fastapi.concurrency import asynccontextmanager
from fastapi import FastAPI
from app.api.router import router
from app.middlewares.request_id import RequestIDMiddleware
from app.middlewares.logging import LoggingMiddleware
from app.core.limiter import limiter

from fastapi.middleware.cors import CORSMiddleware

from app.models.users import User
from app.models.sessions import Session
from app.models.otps import OTP

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.include_router(router)
app.state.limiter = limiter