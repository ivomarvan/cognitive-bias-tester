---
apm_category: task-spec
apm_ref: E010.T030
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T030 — Backend FastAPI skeleton + `/v1/health` + ruff/mypy/pytest config

## Goal

Add the `backend/` service: multi-stage `Dockerfile`, `pyproject.toml` with pinned dependencies, FastAPI app exposing `GET /v1/health`, and a passing test. Configure ruff, `mypy --strict`, pytest. Wire backend into `docker-compose.yml`.

## Inputs

- `.cursor/rules/04-docker-standards.mdc` — multi-stage build template, healthchecks
- `.cursor/rules/10-python.mdc` — Python conventions, type hints, docstrings, dependency justification
- `.cursor/rules/14-fastapi.mdc` — FastAPI structure, lifespan, versioning, error handling, logging
- `.cursor/skills/python-dev/SKILL.md` — running tests inside the container
- T020 outputs: `docker-compose.yml` (db service), `.env.example` with `BACKEND_PORT`

## Outputs

- `backend/Dockerfile` — three stages:
  - `builder` (FROM `python:3.12.3-slim`): installs deps to `/install`
  - `dev` (FROM `python:3.12.3-slim`): copies from builder, adds dev tools (`ruff`, `mypy`, `pytest`, `alembic` placeholder for T040)
  - `production` (FROM `python:3.12.3-slim`): non-root user `appuser`, copies only `src/`, healthcheck via `curl -f http://localhost:8000/v1/health`
- `backend/.dockerignore` — `__pycache__`, `*.pyc`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `tests/`, `.git`, `.env`
- `backend/pyproject.toml`:
  - `[project]` — name `cognitive-bias-tester-backend`, version `0.1.0`, requires-python `>=3.12`
  - `[project.dependencies]` — pinned: `fastapi==0.115.4`, `uvicorn[standard]==0.32.0`, `pydantic==2.9.2`, `pydantic-settings==2.6.1`. Each line has a justification comment.
  - `[project.optional-dependencies] dev` — pinned: `pytest==8.3.3`, `pytest-asyncio==0.24.0`, `httpx==0.27.2`, `ruff==0.7.2`, `mypy==1.13.0`
  - `[tool.ruff]` — `line-length = 100`, `target-version = "py312"`
  - `[tool.ruff.lint]` — `select = ["E", "F", "I", "UP", "B", "SIM"]`
  - `[tool.mypy]` — `python_version = "3.12"`, `strict = true`
  - `[tool.pytest.ini_options]` — `markers = ["unit", "integration", "slow"]`, `addopts = "-q --strict-markers"`
- `backend/src/__init__.py`
- `backend/src/main.py`:
  - `from contextlib import asynccontextmanager`
  - `lifespan` async context manager (placeholder body — comments only, no I/O yet)
  - `app = FastAPI(lifespan=lifespan, title="Cognitive Bias Tester API", version="0.1.0")`
  - registers the health router from `src/api/health.py`
- `backend/src/api/__init__.py`
- `backend/src/api/health.py`:
  - `router = APIRouter(prefix="/v1", tags=["meta"])`
  - `@router.get("/health")` → returns `{"status": "ok", "version": settings.VERSION, "service": "backend"}`
  - Pydantic response model `HealthResponse(BaseModel)` with `status: Literal["ok"]`, `version: str`, `service: str`
  - Full Google-style docstring on the endpoint
- `backend/src/core/__init__.py`
- `backend/src/core/config.py`:
  - `class Settings(BaseSettings)` with `VERSION: str = "0.1.0"`, `LOG_LEVEL: str = "INFO"`, `model_config = SettingsConfigDict(env_file=".env", extra="ignore")`
  - module-level `settings = Settings()` singleton
- `backend/src/core/logging.py` — basic `logging.basicConfig` with structured format; module logger pattern documented
- `backend/tests/__init__.py`
- `backend/tests/test_health.py` — uses `httpx.AsyncClient` and `pytest.mark.unit`; asserts 200 + JSON shape matches `HealthResponse`
- `docker-compose.yml` updated — append `backend` service:
  - `build: { context: ./backend, target: dev }`
  - `env_file: .env`
  - `ports: ["${BACKEND_PORT:-8000}:8000"]`
  - `depends_on: { db: { condition: service_healthy } }`
  - `volumes: ["./backend/src:/app/src"]` (dev hot-reload)
  - `command: uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
  - `healthcheck` curling `/v1/health`
  - `restart: unless-stopped`

## Context Bundle

**Files to read:**
- All four rule files / skill listed in *Inputs*
- `docker-compose.yml` from T020
- `.env.example` from T020 (you'll add `BACKEND_PORT` is already there; if you need new vars, document them too)

**Files NOT to modify:**
- `frontend/`, `nogit_data/`, `experiments/`, `doc/**`
- `.cursor/**`
- `LICENSE`, root `README.md` (T060 finalises READMEs)
- Do **not** introduce DB connection, ORM, or Alembic — those belong to T040

**Interfaces from prior Tasks:**
- T020 exposes the `db` service (PostgreSQL); backend's `depends_on` references it but does **not** connect yet (no DB code in this Task)

## Dependencies

T020.

## Test Specification

- **Happy path:** `pytest -m unit` inside the dev container passes — `test_health.py` returns 200 with valid JSON shape.
- **Edge case (404 default):** `GET /v1/nonexistent` returns 404 with FastAPI's default JSON `{"detail": "Not Found"}`. Add a quick test for this.
- **Quality gate:** `ruff check .`, `ruff format --check .`, `mypy src/ --strict` all return exit code 0 inside the container.

## Definition of Done

See `dod.md`. Summary:
- [ ] `docker compose up backend` runs and `curl localhost:${BACKEND_PORT}/v1/health` returns 200
- [ ] `pytest -m unit` passes inside dev container
- [ ] `ruff check`, `ruff format --check`, `mypy --strict` all pass
- [ ] `Settings` is the single source of config truth
- [ ] All public functions have Google-style docstrings
- [ ] All new tests pass; full suite passes (T010 + T020 + new T030 tests)

## Recommended Coder Model

Composer-2.
