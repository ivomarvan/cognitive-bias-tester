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

- [ ] `.github/workflows/ci.yml` exists with the four jobs: `backend-quality`, `backend-integration`, `frontend-quality`, `docker-build`
- [ ] `backend-integration` job uses `postgres:16.2-alpine` service container with healthcheck
- [ ] All action versions pinned by major (`@v4`, `@v5`, etc.)
- [ ] Triggers: `push` to `main`, `pull_request` to `main`, `workflow_dispatch`
- [ ] `concurrency` group set to cancel superseded runs on the same branch
- [ ] `.github/CODEOWNERS` placeholder created with documented owner field

## Test Criteria

- [ ] YAML parses with `python -c "import yaml; yaml.safe_load(...)"` (exit 0)
- [ ] `actionlint` reports no issues (or noted as not installed in report)
- [ ] No regressions: backend tests, frontend tests, smoke test from T060 still pass

## Code Quality Criteria

- [ ] No `TODO`/`FIXME` in YAML
- [ ] No deploy step (`gh deploy`, `kubectl apply`, etc.) introduced
- [ ] Secret env vars use `${{ secrets.X }}` form — no inline values

## Documentation Criteria

- [ ] `report.md` written with all required sections (in Czech)
- [ ] Code references point to correct lines in `ci.yml`
- [ ] Report explicitly notes that Human must push the branch — Coder did not push

---

**Filled by Coder:** <model-name>, <YYYY-MM-DD>
