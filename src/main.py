import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import engine
from src.models import Base
from src.crud import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("TESTING") != "1":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Cookbook API",
    description="A simple API for managing cooking recipes",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """API root endpoint"""
    return {"message": "Welcome to the simplified Cookbook API!"}
