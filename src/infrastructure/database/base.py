from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config.database import DbConfig

Base = declarative_base()

config = DbConfig()
db_uri = config.get_db_url()
async_engine: AsyncEngine = create_async_engine(url=db_uri, echo=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=async_engine,
                                                                     class_=AsyncSession,
                                                                     expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
