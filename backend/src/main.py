"""FastAPI application entrypoint."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.health import router as health_router
from src.core.config import settings
from src.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan hook (startup/shutdown).

    Placeholder only — persistent resources (DB pool, caches) arrive in later tasks.
    """
    # Startup placeholder: no I/O yet (T040 introduces database connectivity).
    yield
    # Shutdown placeholder: release resources here when they exist.


configure_logging(settings.LOG_LEVEL)

app = FastAPI(
    lifespan=lifespan,
    title="Cognitive Bias Tester API",
    version=settings.VERSION,
)
app.include_router(health_router)
