"""Tests for public meta endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.health import HealthResponse
from src.main import app


@pytest.mark.unit
async def test_health_returns_ok_payload() -> None:
    """``GET /v1/health`` returns 200 and matches ``HealthResponse``."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/health")
    assert response.status_code == 200
    body = response.json()
    parsed = HealthResponse.model_validate(body)
    assert parsed.status == "ok"
    assert parsed.service == "backend"
    assert parsed.version


@pytest.mark.unit
async def test_unknown_route_returns_default_404() -> None:
    """Unregistered paths under ``/v1`` fall back to FastAPI's 404 JSON shape."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
