---
apm_category: epic-plan
apm_ref: E010
apm_level: epic
created_by: Planner
model: claude-opus-4-7
intended_for: Coder, Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Epic Plan: E010 — Repo & Infrastructure Skeleton

## Epic Goal

Bootstrap a production-grade project skeleton: a working Docker Compose environment that brings up PostgreSQL 16, a FastAPI backend with `/v1/health`, a Vue 3 + Vite + Tailwind frontend, plus the surrounding infrastructure (`.gitignore`, `.env.example`, `README.md`, `README.docker.md`, ADRs for the major technical and ethical decisions, and a minimal CI pipeline). After this Epic, every subsequent Epic builds on a stable foundation; **no business logic is implemented in E010**.

The MVP gate is binary: `docker compose up` brings up `db`, `backend`, `frontend` healthy, `curl http://localhost:<backend-port>/v1/health` returns 200, and `ruff` + `mypy --strict` + `pytest` (backend) + `eslint` + `vue-tsc --noEmit` + `vitest` (frontend) all pass on empty skeleton.

## Task List

| Task | Name | Depends on | Coder model |
|------|------|-----------|-------------|
| T010 | Project structure, `.gitignore`, root README skeleton, ADR-001 + ADR-002 | — | Composer-2 |
| T020 | Docker Compose with `db` service + `.env.example` + `README.docker.md` draft | T010 | Composer-2 |
| T030 | Backend FastAPI skeleton + `/v1/health` + ruff/mypy/pytest config | T020 | Composer-2 |
| T040 | Backend DB session + Alembic init | T030 | Composer-2 |
| T050 | Frontend Vue 3 + Vite + Tailwind skeleton + ESLint/Vitest | T020 | Composer-2 |
| T060 | Full-stack integration + final `README.md` and `README.docker.md` | T030, T040, T050 | Composer-2 |
| T070 | CI pipeline (GitHub Actions) | T060 | Composer-2 |

T040 and T050 can be implemented in parallel (different subtrees).

## Cross-Task Conventions

- **Repository layout:** Web-app variant per `06-project-structure.mdc` — `backend/` and `frontend/` at the project root, **not** `src/backend/` and `src/frontend/`.
- **Python version:** 3.12 (set `requires-python = ">=3.12"` in `backend/pyproject.toml`).
- **Node.js version:** 22 LTS (pin in `frontend/Dockerfile` and `frontend/package.json` `engines`).
- **PostgreSQL version:** 16.2-alpine (pin in `docker-compose.yml`).
- **All Docker base images:** pinned versions, no `latest` (per `04-docker-standards.mdc`).
- **Health endpoint URL:** `/v1/health` (versioning from day 1 per `14-fastapi.mdc`).
- **Default ports** (overridable via `.env`): backend `8000`, frontend `5173`, db `5432` (only host-mapped for development convenience; not exposed in production).
- **Service names in compose:** `backend`, `frontend`, `db` (no `api`, `web` aliases — keep names canonical).
- **Branch convention:** all E010 work on `feature/E010-skeleton`. Coder does not commit, push, or merge — Human handles git.

## Task Specifications

---

### T010 — Project structure, `.gitignore`, root README skeleton, ADR-001 + ADR-002

**Goal:**
Lay down the empty directory tree, a comprehensive `.gitignore`, a placeholder root `README.md`, and two Architecture Decision Records (PostgreSQL choice and Ethics framework). After this Task, the repo has structure and rationale but no runnable code yet.

**Inputs:**
- `doc/project-progress/spec.md` — Key Technical Decisions table (referenced by ADRs)
- `doc/project-progress/roadmap.md` — Epic descriptions
- `.cursor/rules/02-git.mdc` — generic `.gitignore` entries
- `.cursor/rules/06-project-structure.mdc` — directory layout
- `.cursor/rules/10-python.mdc` — Python `.gitignore` entries
- `.cursor/rules/11-vuejs-vite-tailwind.mdc` — Node `.gitignore` entries

**Outputs:**
- Directory tree:
  - `backend/` (empty placeholder)
  - `frontend/` (empty placeholder)
  - `doc/architecture/decisions/`
  - `doc/guides/` (empty placeholder)
  - `nogit_data/` (empty placeholder, listed in `.gitignore`)
  - `experiments/` (empty placeholder)
- `.gitignore` (root) — combining generic + Python + Node + Docker + IDE entries
- `README.md` (root) — placeholder with: project name, 1-paragraph description, Quick start (`docker compose up`), link to `doc/project-progress/spec.md`, `LICENSE` mention
- `doc/architecture/decisions/ADR-001-use-postgresql.md` — covers context (multi-user, JSONB needs), decision (PostgreSQL 16 in Docker), consequences (positive/negative), considered alternatives (SQLite — rejected for dev/prod parity). Status: Accepted.
- `doc/architecture/decisions/ADR-002-ethics-framework.md` — covers context (mission of the project), decision (explicit list of B2B segments we will refuse: manipulative-marketing agencies, dark-pattern designers, political microtargeting; positive list of acceptable buyers), consequences. Status: Accepted.
- Empty placeholders use `.gitkeep` files where the directory must exist but contains no real files yet.

**Context Bundle:**
- **Read:** all four rule files listed in *Inputs*; `doc/project-progress/spec.md` Key Technical Decisions section
- **Do not modify:** `.cursor/**` (the submodule), `LICENSE`, `doc/project-progress/brief.md`
- **Interfaces from prior Tasks:** none

**Dependencies:** none

**Test Specification:**
Tests are minimal — file-existence and content-presence checks via a small shell script in `tests/skeleton/test_t010.sh` (executable, returns non-zero on any missing file or missing keyword).

- Happy path: every required file and directory exists.
- Edge case: `.gitignore` contains `__pycache__`, `node_modules`, `.env`, `nogit_data/`.
- ADR check: each ADR has `## Context`, `## Decision`, `## Consequences`, and `**Status**: Accepted`.

**Definition of Done:**
- [ ] All directories listed in *Outputs* exist (with `.gitkeep` where empty)
- [ ] `.gitignore` covers Python, Node, Docker, IDE, OS artifacts, `nogit_data/`
- [ ] Root `README.md` has: title, description, Quick start, license note
- [ ] ADR-001 and ADR-002 have all required sections
- [ ] `tests/skeleton/test_t010.sh` passes
- [ ] Full test suite passes (no regressions — there is nothing else to break yet, but verify manually)

**Recommended Coder model:** Composer-2

---

### T020 — Docker Compose with `db` service, `.env.example`, `README.docker.md` draft

**Goal:**
Create the initial `docker-compose.yml` with PostgreSQL 16 as the only running service. Document environment variables in `.env.example`. Initialise `README.docker.md` with the conventions from `03-docker-policy.mdc`.

**Inputs:**
- `.cursor/rules/03-docker-policy.mdc`
- `.cursor/rules/04-docker-standards.mdc`
- `.cursor/skills/docker-new-project/SKILL.md`

**Outputs:**
- `docker-compose.yml` at project root, containing **only** the `db` service:
  - `image: postgres:16.2-alpine`
  - `env_file: .env`
  - port mapping `${POSTGRES_PORT:-5432}:5432`
  - healthcheck via `pg_isready -U "${POSTGRES_USER}"`
  - named volume `postgres_data`
  - `restart: unless-stopped`
  - **no** `version:` field (obsolete since Compose V2)
- `.env.example` documenting: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, `BACKEND_PORT`, `FRONTEND_PORT` (the latter two reserved for upcoming tasks). Each variable has a one-line comment explaining purpose.
- `README.docker.md` with sections: Quick start, Services table (only `db` for now, with a note "backend and frontend added in T030 / T050"), Common tasks (open psql, run `docker system prune`).
- Update `.gitignore` if needed: `.env` (already present from T010).

**Context Bundle:**
- **Read:** Docker rules + skill listed in *Inputs*; `.gitignore` from T010
- **Do not modify:** files outside the listed outputs; `.cursor/**`
- **Interfaces from prior Tasks:** T010 produced the project root and `.gitignore`

**Dependencies:** T010

**Test Specification:**
- Happy path: `docker compose config` validates successfully with example env values; `docker compose up -d db` brings the service to `(healthy)` within 30 s.
- Edge case: omitting `.env` falls back to the documented defaults in `docker-compose.yml` (use `${VAR:-default}` form for non-secrets).
- Error case: `docker compose config` rejects an obviously invalid `.env` (missing `POSTGRES_PASSWORD`).

The test runner is `tests/skeleton/test_t020.sh` which assumes Docker is available locally; if not, it skips with a non-zero exit only when `--strict` is passed.

**Definition of Done:**
- [ ] `docker compose config` passes with sample `.env`
- [ ] `docker compose up -d db` succeeds and reaches `(healthy)` state
- [ ] `.env.example` documents every required variable
- [ ] `README.docker.md` has Quick start, Services, Common tasks sections
- [ ] No `version:` field in `docker-compose.yml`
- [ ] Image tag is pinned (`postgres:16.2-alpine`, not `:latest`)
- [ ] All new tests pass; full suite passes

**Recommended Coder model:** Composer-2

---

### T030 — Backend FastAPI skeleton + `/v1/health` + ruff/mypy/pytest config

**Goal:**
Add the `backend/` service: multi-stage `Dockerfile`, `pyproject.toml` with pinned dependencies, FastAPI app exposing `GET /v1/health`, one happy-path test. Configure ruff, mypy `--strict`, pytest. Wire backend into `docker-compose.yml`.

**Inputs:**
- `.cursor/rules/04-docker-standards.mdc` — multi-stage build template
- `.cursor/rules/10-python.mdc` — Python conventions, type hints, docstrings
- `.cursor/rules/14-fastapi.mdc` — FastAPI structure, lifespan, versioning, error handling
- `.cursor/skills/python-dev/SKILL.md` — running tests inside the container

**Outputs:**
- `backend/Dockerfile` — three stages (`builder`, `dev`, `production`); pinned `python:3.12.3-slim`; non-root user in production stage
- `backend/.dockerignore`
- `backend/pyproject.toml`:
  - `[project]` requires-python `>=3.12`; deps pinned: `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `httpx` (for tests)
  - `[project.optional-dependencies] dev`: `pytest`, `pytest-asyncio`, `ruff`, `mypy`
  - `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.mypy]` (`strict = true`, `python_version = "3.12"`), `[tool.pytest.ini_options]` with `markers = [unit, integration, slow]`
- `backend/src/__init__.py`
- `backend/src/main.py` — `FastAPI(lifespan=...)` with placeholder lifespan; router registered at `/v1`
- `backend/src/api/health.py` — `APIRouter(prefix="/v1")` with `GET /health` returning `{"status": "ok", "version": "<from pyproject>"}`; full Google-style docstring
- `backend/src/core/config.py` — `Settings(BaseSettings)` reading `.env`
- `backend/tests/test_health.py` — `pytest` test asserting 200 and JSON shape (use FastAPI `TestClient`)
- `docker-compose.yml` updated: add `backend` service with build context, `depends_on: db: condition: service_healthy`, port `${BACKEND_PORT:-8000}:8000`, healthcheck via `curl -f http://localhost:8000/v1/health`
- Backend stage in compose uses `target: dev`

**Context Bundle:**
- **Read:** four rule files listed; `docker-compose.yml` from T020
- **Do not modify:** `frontend/`, `.cursor/**`, anything in `doc/`; do not commit `.env`
- **Interfaces from prior Tasks:** T020's `docker-compose.yml` and `.env.example`

**Dependencies:** T020

**Test Specification:**
- Happy path: `pytest` inside the dev container passes; `GET /v1/health` returns 200 with `{"status": "ok", ...}`.
- Edge case: missing required env variable causes `Settings()` to fail at startup with a clear message.
- Error case: `GET /v1/nonexistent` returns 404 with FastAPI's default JSON.
- Quality gate: `ruff check .`, `ruff format --check .`, `mypy src/ --strict` all return 0.

**Definition of Done:**
- [ ] `docker compose up backend` runs and `curl localhost:${BACKEND_PORT}/v1/health` returns 200
- [ ] `pytest` passes inside the dev container
- [ ] `ruff check`, `ruff format --check`, `mypy --strict` all pass
- [ ] `Settings` is the single source of truth for backend config
- [ ] No `print()` for diagnostics — only `logger.*`
- [ ] All public functions have Google-style docstrings
- [ ] All new tests pass; full suite passes

**Recommended Coder model:** Composer-2

---

### T040 — Backend DB session + Alembic init

**Goal:**
Add async SQLAlchemy session management and Alembic configured for async migrations. Create one empty initial migration so `alembic upgrade head` succeeds against a fresh database.

**Inputs:**
- `.cursor/rules/13-sql-postgresql.mdc` — SQL conventions, repository pattern, psycopg 3
- `.cursor/skills/postgresql-dev/SKILL.md` — Alembic commands

**Outputs:**
- `backend/src/db/__init__.py`
- `backend/src/db/session.py`:
  - Async `create_async_engine(settings.DATABASE_URL, ...)` with pool sized via env
  - `async_sessionmaker[AsyncSession]` factory
  - `async def get_session() -> AsyncIterator[AsyncSession]` dependency for FastAPI
- `backend/alembic.ini` — minimal, points to `alembic/` and uses `${DATABASE_URL}` from env
- `backend/alembic/env.py` — async-aware (using `connectable.run_sync(do_run_migrations)`)
- `backend/alembic/script.py.mako` — default
- `backend/alembic/versions/0001_initial.py` — empty `upgrade()` and `downgrade()` (no schema yet; future Tasks add tables)
- `backend/pyproject.toml` updated: add deps `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `psycopg[binary]` (used by Alembic offline mode if needed) — all pinned
- `backend/Dockerfile` updated: `alembic` available in `dev` and `production` stages
- `backend/src/main.py` updated lifespan: connect via engine on startup, dispose on shutdown
- `backend/tests/test_db.py` — integration test (`@pytest.mark.integration`) that opens a session and runs `SELECT 1`; skipped if `DATABASE_URL` not set
- Update `.env.example`: add `DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` with comment

**Context Bundle:**
- **Read:** rules listed; `backend/` from T030; `docker-compose.yml`
- **Do not modify:** `frontend/`, `.cursor/**`; do not introduce business-logic tables here (those belong to E020)
- **Interfaces from prior Tasks:** T030's `Settings`, FastAPI app, `/v1/health` route

**Dependencies:** T030

**Test Specification:**
- Happy path: `docker compose exec backend alembic upgrade head` exits 0 and creates the `alembic_version` table.
- Edge case: `alembic downgrade base` exits 0 and removes any state.
- Integration: `pytest -m integration tests/test_db.py` connects and runs `SELECT 1`.

**Definition of Done:**
- [ ] `alembic upgrade head` and `alembic downgrade base` both succeed
- [ ] `tests/test_db.py` integration test passes against running `db` service
- [ ] No business-logic tables introduced in this Task (only `alembic_version` from Alembic itself)
- [ ] `Settings.DATABASE_URL` documented in `.env.example`
- [ ] All new tests pass; full suite passes (unit + integration)

**Recommended Coder model:** Composer-2

---

### T050 — Frontend Vue 3 + Vite + Tailwind skeleton + ESLint/Vitest

**Goal:**
Add the `frontend/` service: multi-stage `Dockerfile`, `package.json` with pinned dependencies, Vue 3 + TypeScript-strict + Tailwind + Pinia + vue-router + vue-i18n skeleton, ESLint and Vitest configured. A minimal landing page renders. Wire frontend into `docker-compose.yml`.

**Inputs:**
- `.cursor/rules/04-docker-standards.mdc`
- `.cursor/rules/11-vuejs-vite-tailwind.mdc` — Vue 3 conventions, structure
- `.cursor/skills/vuejs-dev/SKILL.md` — npm / vitest commands

**Outputs:**
- `frontend/Dockerfile` — multi-stage; pinned `node:22.11-alpine` (or a 22.x LTS minor); non-root user in production stage; production stage uses `nginx:1.27-alpine` to serve `dist/`
- `frontend/.dockerignore`
- `frontend/package.json` with `engines.node = ">=22"` and pinned versions of: `vue`, `vue-router`, `pinia`, `vue-i18n`, `tailwindcss`, `vite`, `@vitejs/plugin-vue`, `typescript`, `vue-tsc`, `vitest`, `@vue/test-utils`, `eslint`, `eslint-plugin-vue`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `@vueuse/core`, `autoprefixer`, `postcss`
- `frontend/tsconfig.json` — `"strict": true`
- `frontend/vite.config.ts`
- `frontend/tailwind.config.ts`
- `frontend/postcss.config.cjs`
- `frontend/eslint.config.js` (flat config)
- `frontend/index.html`
- `frontend/src/main.ts` — Vue app + Pinia + Router + i18n
- `frontend/src/App.vue` — root layout
- `frontend/src/router/index.ts`
- `frontend/src/pages/HomePage.vue` — minimalistická landing s nadpisem (anglický text — Tier B human-curated bude doplněn v E040+)
- `frontend/src/locales/{en.json, cs.json}` — placeholder klíče (`app.title`, `home.heading`)
- `frontend/src/components/.gitkeep`
- `frontend/src/composables/.gitkeep`
- `frontend/src/stores/.gitkeep`
- `frontend/src/types/.gitkeep`
- `frontend/src/HomePage.test.ts` collocated next to `HomePage.vue` — Vitest test mounts the page and asserts heading text appears (use `@vue/test-utils`)
- `docker-compose.yml` updated: add `frontend` service; `target: dev`; bind-mount `./frontend/src` for hot reload **only in dev**; port `${FRONTEND_PORT:-5173}:5173`; healthcheck `wget -q --spider http://localhost:5173`

**Context Bundle:**
- **Read:** rules listed; `docker-compose.yml` after T030 (T040 may run in parallel)
- **Do not modify:** `backend/`, `.cursor/**`
- **Interfaces from prior Tasks:** T020's `docker-compose.yml` skeleton and `.env.example`

**Dependencies:** T020 (does **not** depend on T030 — but if both T030 and T050 modify `docker-compose.yml`, Coder runs them serially: T030 first, then T050 appends `frontend` service)

**Test Specification:**
- Happy path: `npm run build` succeeds; `npx vitest run` passes; `npx vue-tsc --noEmit` returns 0; `npx eslint src/` returns 0.
- Edge case: switching `frontend/src/locales` to `cs` updates UI text in `HomePage.vue` test.
- Manual: `docker compose up frontend` and visiting `http://localhost:${FRONTEND_PORT}/` renders the landing page.

**Definition of Done:**
- [ ] `docker compose up frontend` serves the landing page on `${FRONTEND_PORT}`
- [ ] `npm run build` succeeds (production bundle in `dist/`)
- [ ] `npx vue-tsc --noEmit` returns 0
- [ ] `npx eslint src/` returns 0
- [ ] `npx vitest run` passes (at least the `HomePage.test.ts`)
- [ ] All public composables / utilities have TSDoc
- [ ] Tailwind classes work (visible styling on landing page)
- [ ] `vue-i18n` configured with `cs` and `en` placeholder dicts
- [ ] All new tests pass; full suite passes

**Recommended Coder model:** Composer-2

---

### T060 — Full-stack integration + final `README.md` and `README.docker.md`

**Goal:**
Tie everything together. Verify `docker compose up` brings all three services to healthy state. Write the final root `README.md` and complete `README.docker.md` covering all three services.

**Inputs:**
- `.cursor/rules/03-docker-policy.mdc` — README.docker.md required sections
- All outputs from T010–T050

**Outputs:**
- `docker-compose.yml` final review:
  - `depends_on` chains correct: `backend → db (healthy)`, `frontend → backend (healthy)` (frontend doesn't strictly need backend at startup, but include for ordering)
  - All services have `restart: unless-stopped`
  - All services have a healthcheck
  - Networks: default bridge sufficient; no need for explicit network definition
- `README.md` (root) updated to be **production-quality**:
  - Title, project description, "Duolingo for logical thinking" tagline
  - **Status:** MVP under development (E010 complete, see `doc/project-progress/`)
  - Quick start: prerequisites, `cp .env.example .env`, `docker compose up`, expected URLs
  - Project structure (top-level dirs)
  - Documentation links: `doc/project-progress/spec.md`, `doc/project-progress/roadmap.md`, ADRs
  - Contributing: link to `.cursor/README.project_management.md`
  - License
- `README.docker.md` complete:
  - Quick start
  - Services table (db, backend, frontend) with port and description
  - Development vs production builds (`docker compose build --target {dev|production}`)
  - Common tasks: open psql, run alembic migration, open backend shell, frontend npm install workflow, cleanup commands
- `tests/skeleton/test_t060.sh` — runs `docker compose up -d`, polls each service healthcheck, curls `/v1/health` and `http://localhost:${FRONTEND_PORT}/`, then `docker compose down`. Returns 0 on success.

**Context Bundle:**
- **Read:** all outputs from T010–T050; rules listed
- **Do not modify:** `backend/src/**`, `frontend/src/**` (those Tasks are done); only the root-level orchestration files and READMEs
- **Interfaces from prior Tasks:** all of T010–T050

**Dependencies:** T030, T040, T050

**Test Specification:**
- Happy path: `tests/skeleton/test_t060.sh` exits 0.
- Manual: humans verifies the rendered Markdown of both READMEs (proof-read).

**Definition of Done:**
- [ ] `docker compose up` brings all three services to `(healthy)`
- [ ] `tests/skeleton/test_t060.sh` exits 0
- [ ] `README.md` and `README.docker.md` final and proof-read
- [ ] All new tests pass; full suite passes (`pytest` backend + `vitest` frontend)

**Recommended Coder model:** Composer-2

---

### T070 — CI pipeline (GitHub Actions)

**Goal:**
A minimal CI pipeline that runs on every push and pull request to `main` / `feature/**`: lint, type-check, and test both backend and frontend. No deploy in this Task.

**Inputs:**
- `.cursor/rules/02-git.mdc` — branching conventions
- `backend/pyproject.toml` and `frontend/package.json` — defines available scripts
- All outputs from T010–T060

**Outputs:**
- `.github/workflows/ci.yml` with jobs:
  - `backend-quality`: matrix python `3.12`; `ruff check`, `ruff format --check`, `mypy src/ --strict`, `pytest -m "not integration"`
  - `backend-integration`: spins up `postgres:16.2-alpine` service container, runs `alembic upgrade head`, then `pytest -m integration`
  - `frontend-quality`: matrix node `22`; `npm ci`, `npx eslint src/`, `npx vue-tsc --noEmit`, `npx vitest run`, `npm run build`
  - `docker-build`: `docker compose build` (caches via BuildKit) — verifies all Dockerfiles still build; **does not push**
- All jobs use `actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4` (pinned action versions)
- `.github/CODEOWNERS` (placeholder, single-owner)

**Context Bundle:**
- **Read:** all rule files referenced; `pyproject.toml`, `package.json`
- **Do not modify:** `.cursor/**`, anything outside `.github/`
- **Interfaces from prior Tasks:** T030 (backend test commands), T040 (alembic), T050 (frontend test commands), T060 (compose integration)

**Dependencies:** T060

**Test Specification:**
- Happy path: `actionlint` (run locally if available) reports zero issues; YAML parses with `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`.
- Manual on first push: all four jobs succeed on a fresh checkout.

**Definition of Done:**
- [ ] `.github/workflows/ci.yml` exists with the four jobs listed
- [ ] YAML is valid (validated locally)
- [ ] Action versions pinned by major version (`@v4`, `@v5`)
- [ ] `actionlint` (if installed) reports no issues
- [ ] All new tests pass; full suite passes
- [ ] **Note for Human:** first push to GitHub will be a real CI run — Coder must not push; Human pushes after FT.7 approval

**Recommended Coder model:** Composer-2

---

## Cross-Epic Notes for Human

After E010 closes (Phase ER):
- The repository has structure but **no business logic** — that starts in E020.
- The Coder will have produced ADRs 001 and 002. ADR-003 (LLM provider), ADR-004 (embedding model), ADR-005 (hosting), etc., come in later Epics.
- A `feature/E010-skeleton` branch should exist; **all 7 Task commits remain in Coder's working copy until Human reviews and commits**.

## Approval [FE.2]

Before any Task work begins, Human must approve this Epic Plan. Specifically:

- [ ] Task granularity is reasonable (7 Tasks, each ≤ 2 days of solo + AI work)
- [ ] Context Bundles are complete
- [ ] Dependencies are correct
- [ ] No surprises in *Outputs* of any Task
