---
apm_category: task-spec
apm_ref: E010.T020
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T020 — Docker Compose with `db` service, `.env.example`, `README.docker.md` draft

## Goal

Create the initial `docker-compose.yml` with PostgreSQL 16 as the only running service. Document environment variables in `.env.example`. Initialise `README.docker.md` with the conventions from `03-docker-policy.mdc`.

## Inputs

- `.cursor/rules/03-docker-policy.mdc`
- `.cursor/rules/04-docker-standards.mdc`
- `.cursor/skills/docker-new-project/SKILL.md`
- `.gitignore` (root) from T010 — verify `.env` is already excluded

## Outputs

- `docker-compose.yml` at project root, containing **only** the `db` service:
    - `image: postgres:16.2-alpine`
    - `env_file: .env`
    - port mapping `${POSTGRES_PORT:-5432}:5432`
    - healthcheck via `pg_isready -U "${POSTGRES_USER}"`, `interval: 10s`, `timeout: 5s`, `retries: 5`
    - named volume `postgres_data:/var/lib/postgresql/data`
    - `restart: unless-stopped`
    - **no** top-level `version:` field
- `.env.example` documenting (with one-line comment per variable):
    - `POSTGRES_USER=cbt_app`
    - `POSTGRES_PASSWORD=change_me_local_only`
    - `POSTGRES_DB=cognitive_bias_tester`
    - `POSTGRES_PORT=5432`
    - `BACKEND_PORT=8000`  # used in T030
    - `FRONTEND_PORT=5173` # used in T050
- `README.docker.md` with sections:
    - Quick start
    - Services table (only `db` for now; add note: "backend and frontend services added in T030 / T050")
    - Common tasks: open psql, `docker compose down -v` warning, periodic `docker system prune -f`
- `tests/skeleton/test_t020.sh` (executable) — runs `docker compose config` against an `.env` with the example values; if Docker is available locally also runs `docker compose up -d db`, polls healthcheck (max 30 s), then `docker compose down`. Skips Docker-running parts when env var `SKIP_DOCKER_RUN=1` is set.

## Context Bundle

**Files to read:**

- `.cursor/rules/03-docker-policy.mdc`, `04-docker-standards.mdc`, `.cursor/skills/docker-new-project/SKILL.md`
- T010 outputs: root `README.md` (you'll later link to `README.docker.md` from it), `.gitignore`

**Files NOT to modify:**

- `.cursor/**`
- `doc/**`, `LICENSE` — outside this Task's scope
- `backend/`, `frontend/` — those subtrees are owned by T030 / T050; only the root `docker-compose.yml` and its `.env.example` here

**Interfaces from prior Tasks:**

- T010 produced the project root layout, `.gitignore`, and `README.md` with a Quick start that already points at `docker compose up`. This Task makes that command work for the `db` service.

## Dependencies

T010.

## Test Specification

`tests/skeleton/test_t020.sh`:

- **Happy path:** `docker compose config` validates with example env values; `docker compose up -d db` reaches healthy state within 30 s.
- **Edge case (default fallback):** even without `.env` file present, `docker compose config` resolves all `${VAR:-default}` placeholders; **but** services that require secrets (`POSTGRES_PASSWORD`) must fail loudly — verify by removing only `POSTGRES_PASSWORD` and asserting `docker compose config` reports an error or `docker compose up` fails.
- **Error case:** `docker-compose.yml` does **not** contain `version:` field (grep negative check).

## Definition of Done

See `dod.md`. Summary:

- [ ] `docker compose config` passes with sample `.env`
- [ ] `docker compose up -d db` reaches `(healthy)` within 30 s
- [ ] `.env.example` documents every required variable with comments
- [ ] `README.docker.md` has Quick start, Services, Common tasks sections
- [ ] No `version:` field in `docker-compose.yml`
- [ ] PostgreSQL image tag is pinned (`16.2-alpine`)
- [ ] All new tests pass; full suite passes

## Recommended Coder Model

Composer-2.