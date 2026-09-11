from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import DbUrl

engine = create_async_engine(DbUrl)


@asynccontextmanager
async def on_startup(app):
    async with engine.begin() as db:
        from sqlmodel import SQLModel
        await db.run_sync(SQLModel.metadata.create_all)

    yield

    await engine.dispose()


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
