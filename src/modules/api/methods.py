from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.methods import async_engine


async def get_async_session() -> AsyncSession:
    async with async_sessionmaker(async_engine)() as session:
        yield session
