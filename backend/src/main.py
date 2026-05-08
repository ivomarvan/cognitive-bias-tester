"""FastAPI application entrypoint."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_redoc_html
from sqlalchemy import text
from starlette.responses import HTMLResponse

from src.api.health import router as health_router
from src.core.config import settings
from src.core.logging import configure_logging
from src.db.session import engine

logger = logging.getLogger(__name__)

# FastAPI defaults to redoc@next on jsDelivr; that tag often 404s. Use a pinned v2 bundle.
REDOC_STANDALONE_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: verify DB connectivity, dispose engine on shutdown."""
    logger.info("database.verify_reachability.start")
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        logger.exception("database.verify_reachability.failed")
        raise
    logger.info("database.verify_reachability.ok")
    yield
    await engine.dispose()
    logger.info("database.engine_disposed")


configure_logging(settings.LOG_LEVEL)

app = FastAPI(
    lifespan=lifespan,
    title="Cognitive Bias Tester API",
    version=settings.VERSION,
    redoc_url=None,
)
app.include_router(health_router)


@app.get("/redoc", include_in_schema=False)
async def redoc_documentation(request: Request) -> HTMLResponse:
    """Serve ReDoc with a pinned ``redoc.standalone.js`` (default CDN tag breaks).

    Args:
        request: Incoming ASGI request (used for ``root_path`` / OpenAPI URL).

    Returns:
        HTML response that loads ReDoc against ``openapi.json``.
    """
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = f"{root_path}{app.openapi_url}"
    return get_redoc_html(
        openapi_url=openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url=REDOC_STANDALONE_JS_URL,
    )
