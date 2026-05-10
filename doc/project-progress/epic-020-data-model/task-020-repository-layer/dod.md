---
apm_category: dod
apm_ref: E020.T020
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T020 — Repository Layer

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `backend/src/db/repositories/` directory exists with `__init__.py` and one file per entity (10 files total)
- [x] ✅ All repositories extend `Repository[ModelT]` generic base
- [x] ✅ `Repository.add()` uses `session.flush()` (not `commit()`) — caller owns the transaction
- [x] ✅ `Repository.delete()` uses `session.flush()` after `session.delete()`
- [x] ✅ `UiStringRepository.get_all_with_translation(locale)` uses `LEFT OUTER JOIN` (not two separate queries)
- [x] ✅ `UiStringRepository.upsert_translation()` uses PostgreSQL `INSERT ... ON CONFLICT DO UPDATE` (not select-then-insert)
- [x] ✅ `CaseRepository.update_rating()` uses a single `UPDATE` statement (atomic increment, not read-then-write)
- [x] ✅ All repositories accept `AsyncSession` in `__init__` (no global session import)

## Test Criteria

- [x] ✅ `backend/tests/db/test_repositories.py` exists
- [x] ✅ Every public repository method has at least one unit test covering the happy path
- [x] ✅ Every public repository method has at least one unit test covering the empty/None path
- [x] ✅ All tests use `AsyncMock(spec=AsyncSession)` — no live DB dependency
- [x] ✅ All tests are marked `@pytest.mark.unit`
- [x] ✅ `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [x] ✅ `ruff check .` exits 0
- [x] ✅ `ruff format --check .` exits 0
- [x] ✅ `mypy src/ alembic/env.py --strict` exits 0
- [x] ✅ No `TODO` / `FIXME` in committed code
- [x] ✅ All public classes and methods have Google-style docstrings

## Documentation Criteria

- [x] ✅ `report.md` written with all required APM sections
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-10
