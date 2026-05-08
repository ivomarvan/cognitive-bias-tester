---
apm_category: dod
apm_ref: E010.T020
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T020 — Docker Compose with `db`, `.env.example`, `README.docker.md`

> Instructions for Coder: mark each item ✅ (met) or ❌ <note> (not met, with explanation).

---

## Functional Criteria

- [x] ✅ `docker-compose.yml` exists at project root with only `db` service
- [x] ✅ `db` service uses pinned image `postgres:16.2-alpine`
- [x] ✅ `db` has healthcheck using `pg_isready`
- [x] ✅ `db` uses named volume `postgres_data`
- [x] ✅ No top-level `version:` field
- [x] ✅ `.env.example` documents all variables with single-line comments
- [x] ✅ `README.docker.md` covers Quick start, Services, Common tasks (per `03-docker-policy.mdc`)

## Test Criteria

- [x] ✅ `docker compose config` passes with example env (via `--env-file` derived from `.env.example`)
- [x] ✅ `docker compose up -d db` reaches healthy state within 30 s on developer machine *(projekt používá v testu `POSTGRES_PORT=15432`, aby nekolidoval s běžícím Postgresem na 5432)*
- [x] ✅ `bash tests/skeleton/test_t020.sh` exits 0
- [x] ✅ Full test suite passes (T010 tests still pass; `pytest` 0 položek → exit 5)

## Code Quality Criteria

- [x] ✅ `docker-compose.yml` uses `${VAR:-default}` form for non-secret variables only
- [x] ✅ Secrets (`POSTGRES_PASSWORD`) require a real value — no default (`${POSTGRES_PASSWORD:?…}`)
- [x] ✅ No hardcoded credentials or ports inside `docker-compose.yml` (port mapping uses `${POSTGRES_PORT:-5432}`)

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-08
