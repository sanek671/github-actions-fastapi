import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base


if os.environ.get("TESTING") == "1":
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    DATABASE_URL = "sqlite+aiosqlite:///recipes.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session"""
    async with async_session() as session:
        yield session
