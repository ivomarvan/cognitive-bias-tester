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

- [ ] `backend/src/db/session.py` exposes async engine, sessionmaker, `get_session` dependency
- [ ] Alembic configured with async-aware `env.py`
- [ ] `alembic.ini` exists and points to the `alembic/` directory
- [ ] Initial migration `0001_initial.py` is empty (only `pass` in `upgrade`/`downgrade`)
- [ ] `Settings.DATABASE_URL` and `Settings.DB_POOL_SIZE` exist
- [ ] `.env.example` documents `DATABASE_URL` and `DB_POOL_SIZE`
- [ ] FastAPI lifespan verifies DB reachability on startup; disposes on shutdown
- [ ] Production Docker stage has `alembic` available

## Test Criteria

- [ ] `docker compose exec backend alembic upgrade head` exits 0
- [ ] `docker compose exec backend alembic downgrade base` exits 0
- [ ] `pytest -m integration tests/test_db.py` passes
- [ ] `pytest` (unit suite) still passes (no regressions)
- [ ] `mypy src/ --strict` and `ruff check` still pass

## Code Quality Criteria

- [ ] No business-logic ORM models added in this Task
- [ ] All public functions have Google-style docstrings
- [ ] All new dependencies pinned with justification comment
- [ ] No `print()` for diagnostics — logger only

## Documentation Criteria

- [ ] `report.md` written with all required sections (in Czech)
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** <model-name>, <YYYY-MM-DD>
