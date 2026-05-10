---
apm_category: task-spec
apm_ref: E020.T040
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T040 — i18n API Endpoint

## Goal

Implement `GET /v1/i18n/{locale}` — a read-only endpoint that returns all UI chrome translations
for the requested locale, with English fallback for missing or stale translations. No AI calls
are made in this task; the `stale_keys` field in the response signals E040's translation job
which keys need re-translation.

## Depends on

T010 (`UiString`, `UiStringTranslation` models), T020 (`UiStringRepository`).

## Inputs

- `backend/src/db/models/ui_string.py`, `backend/src/db/models/ui_string_translation.py`
- `backend/src/db/repositories/ui_string.py` — especially `get_all_with_translation()`
- `backend/src/db/session.py` — `get_session` FastAPI dependency
- `backend/src/api/health.py` — style reference for FastAPI router pattern
- `backend/src/main.py` — router registration
- `doc/project-progress/spec.md` — UI translation three-tier strategy
- `doc/project-progress/epic-020-data-model/plan.md` — endpoint spec (§ T040)

## Outputs

- `backend/src/api/i18n.py` — FastAPI router + Pydantic response models + resolution logic
- Updated `backend/src/main.py` — `app.include_router(i18n_router)`
- `backend/tests/api/test_i18n.py`

## Implementation Notes

### Router and Pydantic models

```python
# backend/src/api/i18n.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.ui_string import UiStringRepository
from src.db.session import get_session

router = APIRouter(prefix="/v1", tags=["i18n"])


class I18nResponse(BaseModel):
    """Payload returned by GET /v1/i18n/{locale}."""

    locale: str
    translations: dict[str, str]
    stale_keys: list[str]


async def get_ui_string_repo(
    session: AsyncSession = Depends(get_session),
) -> UiStringRepository:
    """FastAPI dependency — instantiate UiStringRepository per request."""
    return UiStringRepository(session)


@router.get("/i18n/{locale}", response_model=I18nResponse)
async def get_i18n(
    locale: str,
    repo: UiStringRepository = Depends(get_ui_string_repo),
) -> I18nResponse:
    """Return all UI string translations for the requested locale.

    Falls back to English source for missing or stale translations.
    Stale keys (hash mismatch) are listed in stale_keys for background re-translation.

    Args:
        locale: IETF language tag, e.g. "en", "cs", "ru".
        repo: UiStringRepository dependency.

    Returns:
        I18nResponse with translations map, stale_keys list, and effective locale.
    """
    ...
```

### Resolution logic (implement in the endpoint or a private helper)

```python
translations: dict[str, str] = {}
stale_keys: list[str] = []

rows = await repo.get_all_with_translation(locale)
for ui_string, translation in rows:
    if locale == "en":
        # Special case: always return English source directly
        translations[ui_string.key] = ui_string.title
    elif translation is None:
        # No translation exists yet — English fallback, NOT stale
        translations[ui_string.key] = ui_string.title
    elif translation.source_hash != ui_string.source_hash:
        # Translation exists but source changed — English fallback + mark stale
        translations[ui_string.key] = ui_string.title
        stale_keys.append(ui_string.key)
    else:
        # Fresh translation
        translations[ui_string.key] = translation.title_translated

return I18nResponse(locale=locale, translations=translations, stale_keys=stale_keys)
```

### main.py update

```python
from src.api.i18n import router as i18n_router
app.include_router(i18n_router)
```

### Locale validation
Do NOT validate that `locale` is a known IETF tag — unknown locales simply fall back to
English. Reject only if `locale` is empty or contains path traversal characters.
Use a simple regex guard: `re.match(r'^[a-zA-Z]{2,8}(-[a-zA-Z0-9]{2,8})*$', locale)`.
Return `422` (FastAPI default) if it doesn't match.

## Test Specification

File: `backend/tests/api/test_i18n.py`

**Integration tests** (marker `integration` — require live DB with seeded UiString data):

```python
@pytest.mark.integration
async def test_get_i18n_english_returns_source_titles(client, seeded_ui_strings) -> None:
    response = await client.get("/v1/i18n/en")
    assert response.status_code == 200
    data = response.json()
    assert data["locale"] == "en"
    assert data["stale_keys"] == []
    assert "app_title" in data["translations"]

@pytest.mark.integration
async def test_get_i18n_unknown_locale_returns_english_fallback(client, seeded_ui_strings) -> None:
    response = await client.get("/v1/i18n/fr")
    assert response.status_code == 200
    data = response.json()
    assert data["stale_keys"] == []  # missing = NOT stale, just fallback

@pytest.mark.integration
async def test_get_i18n_stale_translation_reported(client, seeded_ui_strings_with_stale) -> None:
    # Fixture: one translation with mismatched source_hash
    response = await client.get("/v1/i18n/cs")
    assert response.status_code == 200
    assert "app_title" in response.json()["stale_keys"]

@pytest.mark.integration
async def test_get_i18n_fresh_translation_returned(client, seeded_ui_strings_with_cs) -> None:
    response = await client.get("/v1/i18n/cs")
    data = response.json()
    # One key has fresh cs translation
    assert data["translations"]["app_title"] == "Kognitivní Bias Tester"
    assert "app_title" not in data["stale_keys"]
```

**Unit tests** (marker `unit` — mock repository):

```python
@pytest.mark.unit
async def test_resolution_logic_no_translation_is_not_stale() -> None:
    # Direct test of resolution: translation=None → English fallback, not in stale_keys

@pytest.mark.unit
async def test_resolution_logic_hash_mismatch_is_stale() -> None:
    # translation.source_hash != ui_string.source_hash → key in stale_keys
```

## Regression Check

```bash
ruff check .
ruff format --check .
mypy src/ --strict
pytest -m "not integration" -q
# With live DB:
pytest -m integration -q
```

All must exit 0.

## Definition of Done

See [dod.md](dod.md).
