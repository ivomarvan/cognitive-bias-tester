---
apm_category: dod
apm_ref: E010.T070
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Definition of Done: E010.T070 — CI pipeline (GitHub Actions)

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `.github/workflows/ci.yml` exists with the four jobs: `backend-quality`, `backend-integration`, `frontend-quality`, `docker-build`
- [x] ✅ `backend-integration` job uses `postgres:16.2-alpine` service container with healthcheck
- [x] ✅ All action versions pinned by major (`@v4`, `@v5`, etc.)
- [x] ✅ Triggers: `push` na `main` a `feature/**`, `pull_request` na `main`, `workflow_dispatch`
- [x] ✅ `concurrency` group set to cancel superseded runs on the same branch
- [x] ✅ `.github/CODEOWNERS` placeholder created with documented owner field

## Test Criteria

- [x] ✅ YAML parses with `python -c "import yaml; yaml.safe_load(...)"` (exit 0)
- [x] ✅ `actionlint` bez připomínek (ověřeno přes `docker run rhysd/actionlint:1.7.3 … ci.yml`)
- [x] ✅ No regressions: backend tests, frontend tests, smoke test from T060 still pass

## Code Quality Criteria

- [x] ✅ No `TODO`/`FIXME` in YAML
- [x] ✅ No deploy step (`gh deploy`, `kubectl apply`, etc.) introduced
- [x] ✅ Secret env vars use `${{ secrets.X }}` form — no inline values (není potřeba žádný secret v této úloze)

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in Czech)
- [x] ✅ Code references point to correct lines in `ci.yml`
- [x] ✅ Report explicitly notes that Human must push the branch — Coder did not push

---

**Filled by Coder:** Composer, 2026-05-08
