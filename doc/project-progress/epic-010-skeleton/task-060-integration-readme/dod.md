---
apm_category: dod
apm_ref: E010.T060
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T060 — Full-stack integration + final READMEs

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `docker compose up` brings `db`, `backend`, `frontend` to `(healthy)` within 90 s on a clean machine
- [x] ✅ All three services have working healthchecks
- [x] ✅ `depends_on` chain documented and works (backend waits for db, frontend waits for backend)
- [x] ✅ `README.md` final: title, tagline, status, Quick start, structure, doc links, contributing, license
- [x] ✅ `README.docker.md` final: Quick start, Services table, dev vs production builds, Common tasks
- [x] ✅ `tests/skeleton/test_t060.sh` exists and is executable

## Test Criteria

- [x] ✅ `bash tests/skeleton/test_t060.sh` exits 0
- [x] ✅ Running the smoke test twice in a row both pass
- [x] ✅ Backend `pytest` still passes
- [x] ✅ Frontend `vitest` still passes
- [x] ✅ Backend `mypy --strict`, `ruff check` still pass
- [x] ✅ Frontend `vue-tsc --noEmit`, `eslint` still pass

## Code Quality Criteria

- [x] ✅ No `TODO`/`FIXME` in committed Markdown
- [x] ✅ Service names in compose unchanged (`db`, `backend`, `frontend`)
- [x] ✅ No new application code added in this Task (orchestration + docs only)

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references point to correct files and line numbers
- [x] ✅ `README.md` and `README.docker.md` are the entry points for any new contributor

---

**Filled by Coder:** Composer, 2026-05-08
