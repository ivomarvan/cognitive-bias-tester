---
apm_category: dod
apm_ref: E010.T030
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T030 — Backend FastAPI skeleton

> Instructions for Coder: mark each item ✅ (met) or ❌ <note> (not met, with explanation).

---

## Functional Criteria

- [x] ✅ `backend/Dockerfile` is multi-stage (builder, dev, production); each base image pinned
- [x] ✅ Production stage runs as non-root user
- [x] ✅ `backend/pyproject.toml` has `requires-python = ">=3.12"`
- [x] ✅ All runtime dependencies pinned with justification comment
- [x] ✅ `mypy.strict = true` in pyproject (`[tool.mypy]` → `strict = true`)
- [x] ✅ `ruff` configured per `10-python.mdc`
- [x] ✅ `GET /v1/health` returns `{status, version, service}` matching `HealthResponse` model
- [x] ✅ `Settings` (BaseSettings) reads from `.env` and is the only source of config
- [x] ✅ `docker-compose.yml` `backend` service has healthcheck, `depends_on db: service_healthy`, hot-reload bind-mount *(navíc mount `./backend/tests` kvůli `tests/` v `.dockerignore` — testy v kontejneru musí být na svazku)*

## Test Criteria

- [x] ✅ `pytest -m unit` passes inside dev container (≥ 2 tests: health 200, 404 default)
- [x] ✅ `ruff check` and `ruff format --check` exit 0
- [x] ✅ `mypy src/ --strict` exits 0
- [x] ✅ `docker compose up backend` reaches healthy and returns 200 on `/v1/health` *(v `test_t030.sh`: `db` + `backend`, host port `BACKEND_PORT=18080`, aby se předešlo kolizím)*
- [x] ✅ Full test suite passes — no regressions (`test_t010.sh`, `test_t020.sh`, `test_t030.sh` v jednom běhu → exit **0**)

## Code Quality Criteria

- [x] ✅ No `TODO`/`FIXME` left in committed code
- [x] ✅ All public modules / functions / classes have Google-style docstrings
- [x] ✅ No `print()` for diagnostics — logger only
- [x] ✅ No hardcoded paths, ports, credentials, or magic numbers *(citlivé věci v `.env`; v `docker-compose` je vnitřní port **8000** a cesty `./backend/...` explicitně dle zadání/specifikace služby — mapování na hostitele přes `${BACKEND_PORT:-8000}`)*

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-08
