"""Tests for ``GET /v1/i18n/{locale}``."""

from __future__ import annotations

import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.i18n import build_i18n_payload, validate_locale_path
from src.db.models.ui_string import UiString
from src.db.models.ui_string_translation import UiStringTranslation
from src.db.seed.seed import compute_source_hash
from src.db.session import async_session
from src.main import app


async def _delete_ui_key(session: AsyncSession, key: str) -> None:
    """Remove translation + canonical row for one UI key."""
    await session.execute(delete(UiStringTranslation).where(UiStringTranslation.key == key))
    await session.execute(delete(UiString).where(UiString.key == key))


def _transport() -> ASGITransport:
    """ASGI transport (httpx 0.27 has no ``lifespan`` kwarg on ``ASGITransport``)."""
    return ASGITransport(app=app)


@pytest.mark.unit
def test_resolution_logic_no_translation_is_not_stale() -> None:
    """Missing translation uses English and does not mark stale."""
    ui = UiString(key="k", title="En", description="d", source_hash="h")
    payload = build_i18n_payload("cs", [(ui, None)])
    assert payload.translations["k"] == "En"
    assert payload.stale_keys == []


@pytest.mark.unit
def test_resolution_logic_hash_mismatch_is_stale() -> None:
    """Stale hash uses English title and lists the key."""
    ui = UiString(key="k", title="En", description="d", source_hash="new")
    tr = UiStringTranslation(
        key="k",
        locale="cs",
        title_translated="Cs",
        description_translated=None,
        source_hash="old",
    )
    payload = build_i18n_payload("cs", [(ui, tr)])
    assert payload.translations["k"] == "En"
    assert payload.stale_keys == ["k"]


@pytest.mark.unit
def test_resolution_logic_english_never_stale() -> None:
    """English locale always mirrors source titles."""
    ui = UiString(key="k", title="En", description="d", source_hash="x")
    stale = UiStringTranslation(
        key="k",
        locale="en",
        title_translated="Wrong",
        description_translated=None,
        source_hash="y",
    )
    payload = build_i18n_payload("en", [(ui, stale)])
    assert payload.translations["k"] == "En"
    assert payload.stale_keys == []


@pytest.mark.unit
def test_validate_locale_rejects_empty() -> None:
    """Invalid locale raises HTTPException 422."""
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc:
        validate_locale_path("")
    assert exc.value.status_code == 422


@pytest.mark.integration
async def test_get_i18n_english_returns_source_titles() -> None:
    """English request returns source titles and empty stale list."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    keys = ["app_title", "home_heading"]
    title_app = "Cognitive Bias Tester"
    desc_app = "app desc"
    hash_app = compute_source_hash("app_title", title_app, desc_app)
    title_home = "Welcome"
    desc_home = "home desc"
    hash_home = compute_source_hash("home_heading", title_home, desc_home)

    async with async_session() as session, session.begin():
        for k in keys:
            await _delete_ui_key(session, k)
        session.add(
            UiString(
                key="app_title",
                title=title_app,
                description=desc_app,
                source_hash=hash_app,
            )
        )
        session.add(
            UiString(
                key="home_heading",
                title=title_home,
                description=desc_home,
                source_hash=hash_home,
            )
        )

    transport = _transport()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/i18n/en")

    assert response.status_code == 200
    data = response.json()
    assert data["locale"] == "en"
    assert data["stale_keys"] == []
    assert data["translations"]["app_title"] == title_app

    async with async_session() as session, session.begin():
        for k in keys:
            await _delete_ui_key(session, k)


@pytest.mark.integration
async def test_get_i18n_unknown_locale_returns_english_fallback() -> None:
    """Locale with no rows falls back to English; missing keys are not stale."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    title_app = "English Only"
    desc_app = "d"
    hash_app = compute_source_hash("app_title", title_app, desc_app)

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")
        session.add(
            UiString(
                key="app_title",
                title=title_app,
                description=desc_app,
                source_hash=hash_app,
            )
        )

    transport = _transport()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/i18n/fr")

    assert response.status_code == 200
    data = response.json()
    assert data["stale_keys"] == []
    assert data["translations"]["app_title"] == title_app

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")


@pytest.mark.integration
async def test_get_i18n_stale_translation_reported() -> None:
    """Mismatched source_hash yields English text and stale key."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    title_app = "English App"
    desc_app = "d"
    hash_fresh = compute_source_hash("app_title", title_app, desc_app)

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")
        session.add(
            UiString(
                key="app_title",
                title=title_app,
                description=desc_app,
                source_hash=hash_fresh,
            )
        )
        session.add(
            UiStringTranslation(
                key="app_title",
                locale="cs",
                title_translated="Old Czech",
                description_translated=None,
                source_hash="outdated_hash_value",
            )
        )

    transport = _transport()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/i18n/cs")

    assert response.status_code == 200
    body = response.json()
    assert "app_title" in body["stale_keys"]
    assert body["translations"]["app_title"] == title_app

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")


@pytest.mark.integration
async def test_get_i18n_fresh_translation_returned() -> None:
    """Matching hash returns translated title and excludes stale list."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    title_app = "English App"
    desc_app = "d"
    hash_app = compute_source_hash("app_title", title_app, desc_app)
    cs_title = "Kognitivní Bias Tester"

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")
        session.add(
            UiString(
                key="app_title",
                title=title_app,
                description=desc_app,
                source_hash=hash_app,
            )
        )
        session.add(
            UiStringTranslation(
                key="app_title",
                locale="cs",
                title_translated=cs_title,
                description_translated=None,
                source_hash=hash_app,
            )
        )

    transport = _transport()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/i18n/cs")

    assert response.status_code == 200
    data = response.json()
    assert data["translations"]["app_title"] == cs_title
    assert "app_title" not in data["stale_keys"]

    async with async_session() as session, session.begin():
        await _delete_ui_key(session, "app_title")


@pytest.mark.integration
async def test_get_i18n_invalid_locale_422() -> None:
    """Malformed locale tags return 422."""
    if not os.environ.get("DATABASE_URL"):
        pytest.skip("DATABASE_URL is not set")

    transport = _transport()
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/v1/i18n/123numeric")
    assert response.status_code == 422
