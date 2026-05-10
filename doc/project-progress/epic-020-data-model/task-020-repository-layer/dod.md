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

- [ ] `backend/src/db/repositories/` directory exists with `__init__.py` and one file per entity (10 files total)
- [ ] All repositories extend `Repository[ModelT]` generic base
- [ ] `Repository.add()` uses `session.flush()` (not `commit()`) — caller owns the transaction
- [ ] `Repository.delete()` uses `session.flush()` after `session.delete()`
- [ ] `UiStringRepository.get_all_with_translation(locale)` uses `LEFT OUTER JOIN` (not two separate queries)
- [ ] `UiStringRepository.upsert_translation()` uses PostgreSQL `INSERT ... ON CONFLICT DO UPDATE` (not select-then-insert)
- [ ] `CaseRepository.update_rating()` uses a single `UPDATE` statement (atomic increment, not read-then-write)
- [ ] All repositories accept `AsyncSession` in `__init__` (no global session import)

## Test Criteria

- [ ] `backend/tests/db/test_repositories.py` exists
- [ ] Every public repository method has at least one unit test covering the happy path
- [ ] Every public repository method has at least one unit test covering the empty/None path
- [ ] All tests use `AsyncMock(spec=AsyncSession)` — no live DB dependency
- [ ] All tests are marked `@pytest.mark.unit`
- [ ] `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [ ] `ruff check .` exits 0
- [ ] `ruff format --check .` exits 0
- [ ] `mypy src/ --strict` exits 0
- [ ] No `TODO` / `FIXME` in committed code
- [ ] All public classes and methods have Google-style docstrings

## Documentation Criteria

- [ ] `report.md` written with all required APM sections
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** _______________, ___________
