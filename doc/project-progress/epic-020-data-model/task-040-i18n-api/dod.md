---
apm_category: dod
apm_ref: E020.T040
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T040 — i18n API Endpoint

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `GET /v1/i18n/{locale}` endpoint exists in `backend/src/api/i18n.py`
- [x] ✅ `backend/src/main.py` includes the i18n router
- [x] ✅ `locale == "en"` always returns English source titles with `stale_keys: []`
- [x] ✅ Unknown locale (e.g. `fr` with no translations) returns English fallback for all keys and `stale_keys: []` (missing ≠ stale)
- [x] ✅ Translation with matching `source_hash` → returns `title_translated` and is NOT in `stale_keys`
- [x] ✅ Translation with mismatched `source_hash` → returns English fallback AND key appears in `stale_keys`
- [x] ✅ Invalid locale format (e.g. empty string, path traversal) → `422 Unprocessable Entity`
- [x] ✅ No AI translation calls are made in this endpoint
- [x] ✅ Response is validated by `I18nResponse` Pydantic model (`locale`, `translations`, `stale_keys`)

## Test Criteria

- [x] ✅ `backend/tests/api/test_i18n.py` exists
- [x] ✅ At least 4 integration tests covering: English locale, unknown locale fallback, stale translation, fresh translation
- [x] ✅ At least 2 unit tests covering resolution logic with mocked repository
- [x] ✅ Integration tests marked `@pytest.mark.integration`; unit tests marked `@pytest.mark.unit`
- [x] ✅ `pytest -m "not integration" -q` exits 0
- [x] ✅ `pytest -m integration -q` exits 0 (with live DB) — ověřeno v CI; lokálně vyžaduje konzistentní Alembic stav DB

## Code Quality Criteria

- [x] ✅ `ruff check .` exits 0
- [x] ✅ `ruff format --check .` exits 0
- [x] ✅ `mypy src/ --strict` exits 0
- [x] ✅ No `TODO` / `FIXME` in committed code
- [x] ✅ Endpoint and Pydantic models have Google-style docstrings

## Documentation Criteria

- [x] ✅ `report.md` written with all required APM sections
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-10
