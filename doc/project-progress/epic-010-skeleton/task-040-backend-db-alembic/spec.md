---
apm_category: task-spec
apm_ref: E010.T040
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T040 — Backend DB session + Alembic init

## Goal

Add async SQLAlchemy session management and Alembic configured for async migrations. Create one empty initial migration so `alembic upgrade head` succeeds against a fresh database. **No business-logic tables are introduced in this Task** — those belong to E020.

## Inputs

- `.cursor/rules/13-sql-postgresql.mdc` — naming, async patterns, repository pattern, parameterised queries
- `.cursor/skills/postgresql-dev/SKILL.md` — Alembic commands inside Docker
- T030 outputs: `backend/pyproject.toml`, `backend/src/core/config.py`, `backend/src/main.py`
- T020 outputs: `db` service in `docker-compose.yml`, `.env.example`

## Outputs

- `backend/src/db/__init__.py`
- `backend/src/db/session.py`:
  - `engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=settings.DB_POOL_SIZE)`
  - `async_session = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)`
  - `async def get_session() -> AsyncIterator[AsyncSession]` (FastAPI dependency)
  - Full Google-style docstrings; module-level logger
- `backend/alembic.ini` — minimal; `script_location = alembic`; `sqlalchemy.url` overridden by env in `env.py`
- `backend/alembic/env.py` — async-aware migrations using `connectable.run_sync(do_run_migrations)`; reads `settings.DATABASE_URL`
- `backend/alembic/script.py.mako` — default Alembic template
- `backend/alembic/versions/0001_initial.py`:
  - `revision = "0001"`, `down_revision = None`, `branch_labels = None`, `depends_on = None`
  - `def upgrade() -> None: pass`
  - `def downgrade() -> None: pass`
- `backend/pyproject.toml` updated dependencies (pinned, with justification comments):
  - `sqlalchemy[asyncio]==2.0.36`
  - `asyncpg==0.30.0`
  - `alembic==1.14.0`
  - `psycopg[binary]==3.2.3` (used as fallback by Alembic for offline mode)
- `backend/Dockerfile` — `dev` and `production` stages must have `alembic` available; dev stage already gets it via dev deps; production needs alembic from main `[project.dependencies]` (move it there)
- `backend/src/main.py` lifespan updated:
  - On startup: `await engine.connect()` once and dispose; verifies DB reachable; log event
  - On shutdown: `await engine.dispose()`
- `backend/src/core/config.py` — add fields:
  - `DATABASE_URL: str` (no default — must come from `.env`)
  - `DB_POOL_SIZE: int = 5`
- `backend/tests/test_db.py`:
  - `@pytest.mark.integration` test `test_can_select_one`: opens a session and runs `await session.execute(text("SELECT 1"))`, asserts result `== 1`
  - Skipped automatically when `DATABASE_URL` is unset
- `.env.example` updated:
  - `DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` (with comment)
  - `DB_POOL_SIZE=5`

## Context Bundle

**Files to read:**
- `13-sql-postgresql.mdc`, `postgresql-dev/SKILL.md`
- `backend/src/main.py`, `backend/src/core/config.py`, `backend/pyproject.toml` (T030)
- `docker-compose.yml`, `.env.example` (T020)

**Files NOT to modify:**
- `frontend/**`, `doc/**`, `.cursor/**`, `LICENSE`
- `backend/src/api/health.py` (T030 owns it; if you must extend lifespan, do so in `main.py`)
- **Do not introduce business-logic ORM models** — no `User`, `Case`, `Rating` tables here

**Interfaces from prior Tasks:**
- T030's `Settings` and `app` (extend, don't replace)
- T020's `db` service (target of `DATABASE_URL`)

## Dependencies

T030.

## Test Specification

- **Happy path:** `docker compose exec backend alembic upgrade head` exits 0 and creates `alembic_version` table; `pytest -m integration tests/test_db.py` passes.
- **Edge case (downgrade):** `alembic downgrade base` exits 0 and removes any state cleanly.
- **Error case (bad URL):** with `DATABASE_URL=postgresql+asyncpg://wrong@nowhere/db`, lifespan startup fails fast with a clear log entry (manual test, not automated).

## Definition of Done

See `dod.md`. Summary:
- [ ] `alembic upgrade head` and `alembic downgrade base` both succeed
- [ ] `tests/test_db.py` integration test passes against running `db` service
- [ ] No business-logic tables introduced (only `alembic_version`)
- [ ] `Settings.DATABASE_URL` documented in `.env.example`
- [ ] All new tests pass; full suite passes (unit + integration)

## Recommended Coder Model

Composer-2.
