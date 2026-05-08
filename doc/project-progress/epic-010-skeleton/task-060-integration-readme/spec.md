---
apm_category: task-spec
apm_ref: E010.T060
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T060 — Full-stack integration + final `README.md` and `README.docker.md`

## Goal

Tie all three services together. Verify `docker compose up` brings `db`, `backend`, `frontend` to healthy state. Write the **final** root `README.md` and complete `README.docker.md`. Add a smoke-test script that automates the whole stack-up / stack-down cycle.

## Inputs

- `.cursor/rules/03-docker-policy.mdc` — required `README.docker.md` sections
- All outputs from T010, T020, T030, T040, T050

## Outputs

- `docker-compose.yml` final review:
  - `depends_on` chains: `backend → db (service_healthy)`; `frontend → backend (service_healthy)` (frontend doesn't strictly need backend, but include for readable startup order)
  - All services have `restart: unless-stopped`
  - All services have a `healthcheck`
  - No explicit `networks:` section (default bridge is sufficient for MVP)
  - All env vars come from `.env`
- `README.md` (root) — production-quality:
  - Title, tagline ("Duolingo for logical thinking")
  - **Status:** *MVP under development — Epic E010 (skeleton) complete, see `doc/project-progress/`*
  - Quick start: prerequisites (Docker + Docker Compose v2), `cp .env.example .env`, `docker compose up`, expected URLs (backend health at `http://localhost:8000/v1/health`, frontend at `http://localhost:5173/`)
  - Project structure (top-level dirs: `backend/`, `frontend/`, `doc/`, …)
  - Documentation links: `doc/project-progress/spec.md`, `doc/project-progress/roadmap.md`, ADRs in `doc/architecture/decisions/`
  - Development workflow: link to `.cursor/skills/python-dev/`, `.cursor/skills/vuejs-dev/`, `README.docker.md`
  - Contributing: link to `.cursor/README.project_management.md`
  - License (`MIT`, see `LICENSE`)
- `README.docker.md` — complete:
  - Quick start
  - Services table:
    | Service | Port (host) | Description | Healthcheck |
    |---------|-------------|-------------|-------------|
    | `db`    | 5432        | PostgreSQL 16.2 | `pg_isready` |
    | `backend` | 8000      | FastAPI       | `curl /v1/health` |
    | `frontend` | 5173     | Vue 3 + Vite (dev) | `wget --spider /` |
  - Development vs production builds (`docker compose build --target dev` vs `--target production`)
  - Common tasks: `docker compose exec db psql`, `docker compose exec backend pytest`, `docker compose exec backend alembic upgrade head`, `docker compose exec frontend npm install <pkg>`, cleanup (`docker system prune`, `docker volume prune`)
- `tests/skeleton/test_t060.sh` (executable):
  - `docker compose up -d`
  - poll `db` healthcheck up to 30 s
  - poll `backend` healthcheck up to 60 s; `curl localhost:${BACKEND_PORT:-8000}/v1/health` must return 200 with valid JSON
  - poll `frontend` healthcheck up to 60 s; `curl localhost:${FRONTEND_PORT:-5173}/` must return 200
  - `docker compose down`
  - exit 0 on success, non-zero on any failure with descriptive log

## Context Bundle

**Files to read:**
- All outputs of T010–T050
- `.cursor/rules/03-docker-policy.mdc`

**Files NOT to modify:**
- `backend/src/**`, `frontend/src/**` — those subtrees are owned by T030 / T040 / T050 and are complete
- `doc/project-progress/{spec,roadmap,brief,GLOSSARY}.md`
- ADRs in `doc/architecture/decisions/` (T010 owns them)
- `.cursor/**`, `LICENSE`

**Interfaces from prior Tasks:**
- All five prior Tasks. This Task is purely orchestration + documentation; no new application code.

## Dependencies

T030, T040, T050.

## Test Specification

- **Happy path:** `bash tests/skeleton/test_t060.sh` exits 0 on a clean checkout (after `cp .env.example .env`).
- **Edge case (image rebuild):** running the test twice in a row both pass (first build, second uses cache).
- **Manual:** Human visits both URLs in a browser; landing page renders; backend health JSON visible.

## Definition of Done

See `dod.md`. Summary:
- [ ] `docker compose up` brings all three services to `(healthy)`
- [ ] `tests/skeleton/test_t060.sh` exits 0
- [ ] `README.md` and `README.docker.md` final and proof-read
- [ ] All new tests pass; full suite passes (backend `pytest` + frontend `vitest`)

## Recommended Coder Model

Composer-2.
