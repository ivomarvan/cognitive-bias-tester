"""Versioned health check endpoint."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.core.config import settings

router = APIRouter(prefix="/v1", tags=["meta"])


class HealthResponse(BaseModel):
    """Payload returned by ``GET /v1/health``."""

    status: Literal["ok"] = Field(description="Liveness flag for probes.")
    version: str = Field(description="Semantic API version string.")
    service: str = Field(description="Logical service name.")


@router.get("/health", response_model=HealthResponse)
async def read_health() -> HealthResponse:
    """Return a minimal heartbeat payload for orchestrators and smoke tests.

    Returns:
        HealthResponse: Constant ``ok`` status with the running API version.
    """
    return HealthResponse(status="ok", version=settings.VERSION, service="backend")
