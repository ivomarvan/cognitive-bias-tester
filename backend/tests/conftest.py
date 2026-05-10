"""Pytest configuration: set required environment variables before src imports.

DATABASE_URL must be present so that ``pydantic_settings.Settings()`` can
instantiate during module import — even in the ``backend-quality`` CI job that
runs without a live PostgreSQL service.  The value is a valid DSN string so
that SQLAlchemy can build an engine object; the actual network connection is
never opened during unit tests (ASGITransport in httpx does not trigger the
ASGI lifespan, and model-only tests never touch the session).
"""
import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://test:test@localhost:5432/test",
)
