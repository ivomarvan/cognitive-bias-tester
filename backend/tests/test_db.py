"""Integration tests against PostgreSQL (requires DATABASE_URL and a running db)."""

import os

import pytest
from sqlalchemy import text


@pytest.mark.integration
async def test_can_select_one() -> None:
    """Opening a session and running ``SELECT 1`` returns a single row with value 1."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    from src.db.session import async_session

    async with async_session() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1
