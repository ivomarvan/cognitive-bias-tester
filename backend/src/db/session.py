"""Async SQLAlchemy engine and request-scoped session dependency."""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings

logger = logging.getLogger(__name__)

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
)
logger.info(
    "database.engine_configured pool_size=%s url_scheme=%s",
    settings.DB_POOL_SIZE,
    settings.DATABASE_URL.split(":", 1)[0],
)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an ``AsyncSession`` for the current request (FastAPI ``Depends``).

    Args:
        None — the caller injects this generator via ``Depends(get_session)``.

    Yields:
        Database session with ``expire_on_commit=False`` for safe reads after commit.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: Propagated when the session cannot be opened
            or the surrounding transaction fails.
    """
    async with async_session() as session:
        yield session
