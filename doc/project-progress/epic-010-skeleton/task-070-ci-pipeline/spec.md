---
apm_category: task-spec
apm_ref: E010.T070
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T070 — CI pipeline (GitHub Actions)

## Goal

A minimal CI pipeline triggered on push and pull request to `main` and `feature/**`: lint, type-check, and test both backend and frontend; verify Docker builds. **No deploy step in this Task.** Coder writes the YAML file but does **not** push to GitHub — Human pushes after FT.7 approval.

## Inputs

- `.cursor/rules/02-git.mdc` — branching conventions
- All outputs from T010–T060 — defines what to lint/test/build

## Outputs

- `.github/workflows/ci.yml` with these jobs (all on `ubuntu-24.04`):
  1. **`backend-quality`**:
     - matrix python `["3.12"]`
     - steps: checkout, setup-python, install backend deps from `pyproject.toml` (`pip install -e ./backend[dev]`), `cd backend && ruff check .`, `ruff format --check .`, `mypy src/ --strict`, `pytest -m "not integration" -q`
  2. **`backend-integration`**:
     - service container `postgres:16.2-alpine` with healthcheck
     - env: `DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/test`
     - steps: checkout, setup-python, install backend deps, `cd backend && alembic upgrade head`, `pytest -m integration -q`
  3. **`frontend-quality`**:
     - matrix node `["22"]`
     - steps: checkout, setup-node with cache, `cd frontend && npm ci`, `npx eslint src/`, `npx vue-tsc --noEmit`, `npx vitest run`, `npm run build`
  4. **`docker-build`**:
     - steps: checkout, setup-buildx, `docker compose -f docker-compose.yml build` (uses BuildKit cache via `actions/cache`)
- All action versions pinned by major: `actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`, `docker/setup-buildx-action@v3`, `actions/cache@v4`
- Triggers: `push` to `main`, `pull_request` targeting `main`, manual `workflow_dispatch`
- `concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }`
- `.github/CODEOWNERS` placeholder with single owner (`* @ivomarvan` — but use a generic `@OWNER` placeholder if Coder doesn't know the GitHub handle; document the placeholder for Human to replace)

## Context Bundle

**Files to read:**
- `02-git.mdc`
- `backend/pyproject.toml` — confirms test commands and Python version
- `frontend/package.json` — confirms scripts and Node version
- `docker-compose.yml` — confirms image build context

**Files NOT to modify:**
- Anything outside `.github/`
- `.cursor/**`, `LICENSE`

**Interfaces from prior Tasks:**
- Backend: `pytest -m "not integration"` for unit, `pytest -m integration` for DB-required tests
- Frontend: `npx vitest run`, `npx vue-tsc --noEmit`, `npx eslint src/`, `npm run build`

## Dependencies

T060.

## Test Specification

- **Local validation:**
  - `python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` exits 0
  - If `actionlint` is installed locally, it reports zero issues
- **Manual on first push (post-approval, by Human):**
  - All four jobs succeed on `feature/E010-skeleton`
  - Failing test (manually break one) causes the corresponding job to fail
  - Pipeline must not run on `.cursor/**` changes only — irrelevant — but it does not need to skip them either; just must not error on them

## Definition of Done

See `dod.md`. Summary:
- [ ] `.github/workflows/ci.yml` with all four jobs
- [ ] YAML is valid
- [ ] Action versions pinned by major
- [ ] No deploy step
- [ ] `actionlint` (if installed) reports no issues
- [ ] All new tests pass; full suite passes (locally)
- [ ] **Human note:** first push pending Human approval

## Recommended Coder Model

Composer-2.
