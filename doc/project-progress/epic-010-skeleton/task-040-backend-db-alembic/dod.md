---
apm_category: dod
apm_ref: E010.T040
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T040 — Backend DB session + Alembic init

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `backend/src/db/session.py` exposes async engine, sessionmaker, `get_session` dependency
- [x] ✅ Alembic configured with async-aware `env.py`
- [x] ✅ `alembic.ini` exists and points to the `alembic/` directory
- [x] ✅ Initial migration `0001_initial.py` is empty (`upgrade`/`downgrade` = `pass` only)
- [x] ✅ `Settings.DATABASE_URL` and `Settings.DB_POOL_SIZE` exist
- [x] ✅ `.env.example` documents `DATABASE_URL` and `DB_POOL_SIZE`
- [x] ✅ FastAPI lifespan verifies DB reachability on startup; disposes engine on shutdown
- [x] ✅ Production Docker stage has `alembic` on disk (`alembic.ini` + `alembic/`) and runtime deps include `alembic` / `psycopg` via `pyproject.toml`

## Test Criteria

- [x] ✅ `docker compose exec backend alembic upgrade head` exits 0 (viz `tests/skeleton/test_t040.sh`)
- [x] ✅ `docker compose exec backend alembic downgrade base` exits 0
- [x] ✅ `pytest -m integration tests/test_db.py` passes
- [x] ✅ `pytest` (unit suite) still passes (no regressions)
- [x] ✅ `mypy src/ alembic/env.py --strict` and `ruff check` still pass (`pydantic.mypy` plugin for `Settings()`)

## Code Quality Criteria

- [x] ✅ No business-logic ORM models added in this Task
- [x] ✅ All public functions have Google-style docstrings
- [x] ✅ All new dependencies pinned with justification comment in `pyproject.toml`
- [x] ✅ No `print()` for diagnostics — logger only

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-08
