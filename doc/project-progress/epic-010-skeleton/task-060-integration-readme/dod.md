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

- [ ] `docker compose up` brings `db`, `backend`, `frontend` to `(healthy)` within 90 s on a clean machine
- [ ] All three services have working healthchecks
- [ ] `depends_on` chain documented and works (backend waits for db, frontend waits for backend)
- [ ] `README.md` final: title, tagline, status, Quick start, structure, doc links, contributing, license
- [ ] `README.docker.md` final: Quick start, Services table, dev vs production builds, Common tasks
- [ ] `tests/skeleton/test_t060.sh` exists and is executable

## Test Criteria

- [ ] `bash tests/skeleton/test_t060.sh` exits 0
- [ ] Running the smoke test twice in a row both pass
- [ ] Backend `pytest` still passes
- [ ] Frontend `vitest` still passes
- [ ] Backend `mypy --strict`, `ruff check` still pass
- [ ] Frontend `vue-tsc --noEmit`, `eslint` still pass

## Code Quality Criteria

- [ ] No `TODO`/`FIXME` in committed Markdown
- [ ] Service names in compose unchanged (`db`, `backend`, `frontend`)
- [ ] No new application code added in this Task (orchestration + docs only)

## Documentation Criteria

- [ ] `report.md` written with all required sections (in Czech)
- [ ] Code references point to correct files and line numbers
- [ ] `README.md` and `README.docker.md` are the entry points for any new contributor

---

**Filled by Coder:** <model-name>, <YYYY-MM-DD>
