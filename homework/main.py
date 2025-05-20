import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine
from models import Base
from crud import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events for the application"""
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

# Run app with: uvicorn main:app --reload