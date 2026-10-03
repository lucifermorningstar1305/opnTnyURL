from typing import Literal, cast

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.config import Settings
from app.logger.logger import RichLogger

async_eng = create_async_engine(
    Settings.ASYNC_POSTGRES_URL,
    pool_size=6,
    max_overflow=5,
    pool_timeout=30,
    pool_pre_ping=True,
)

AsyncLocal = async_sessionmaker(
    bind=async_eng, class_=AsyncSession, expire_on_commit=False
)

logger = RichLogger(
    name="backend.db",
    log_lvl=cast(Literal["info", "debug", "warning", "error"], Settings.LOG_LEVEL),
)


async def get_session():
    async with AsyncLocal() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise


async def close_async_engine():
    await async_eng.dispose()


async def connection_check():
    try:
        async with async_eng.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info(msg="✅ Successfully connected to the database!")
    except SQLAlchemyError as e:
        logger.error(msg=f"❌ Error connecting to database: {e}")
