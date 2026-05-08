---
apm_category: task-spec
apm_ref: E010.T010
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Specification: E010.T010 — Project structure, `.gitignore`, root `README.md` skeleton, ADR-001 + ADR-002

## Goal

Lay down the empty directory tree, a comprehensive root `.gitignore`, a placeholder root `README.md`, and two Architecture Decision Records (ADR-001 PostgreSQL choice, ADR-002 Ethics framework). After this Task, the repo has structure and rationale but no runnable code yet.

## Inputs

- `doc/project-progress/spec.md` — Key Technical Decisions table (referenced by ADR-001 and ADR-002)
- `doc/project-progress/roadmap.md` — Epic descriptions
- `.cursor/rules/02-git.mdc` — generic `.gitignore` entries
- `.cursor/rules/06-project-structure.mdc` — directory layout for web-app project
- `.cursor/rules/10-python.mdc` — Python `.gitignore` section
- `.cursor/rules/11-vuejs-vite-tailwind.mdc` — Node `.gitignore` section

## Outputs

- Directory tree at project root (web-app layout per `06-project-structure.mdc`):
  - `backend/.gitkeep`
  - `frontend/.gitkeep`
  - `doc/architecture/decisions/` (no `.gitkeep`; ADRs go here)
  - `doc/guides/.gitkeep`
  - `doc/external/.gitkeep`
  - `nogit_data/.gitkeep` *(this `.gitkeep` is the only file ever committed in `nogit_data/`; the directory itself is in `.gitignore`)*
  - `experiments/.gitkeep`
  - `tests/skeleton/` (will hold `test_t010.sh` from this Task and later `test_t020.sh`, `test_t060.sh`)
- `.gitignore` (root) — comprehensive, combining: secrets/env, IDE, OS artifacts, `nogit_data/` (keep `.gitkeep`), generic logs, Python, Node, Docker, generated docs (per the language/framework rules)
- `README.md` (root) — placeholder with: title, 1-paragraph description, "Status: MVP under development", Quick start (`cp .env.example .env && docker compose up`), project structure (`backend/`, `frontend/`, `doc/`, …), link to `doc/project-progress/spec.md` and `doc/project-progress/roadmap.md`, license note (MIT — already in `LICENSE` at repo root)
- `doc/architecture/decisions/ADR-001-use-postgresql.md`
- `doc/architecture/decisions/ADR-002-ethics-framework.md`
- `tests/skeleton/test_t010.sh` (executable) — file-existence checks; returns non-zero on first missing file or missing keyword

## Context Bundle

**Files to read:**
- All four rule files listed in *Inputs* — `.gitignore` entries, directory layout
- `doc/project-progress/spec.md` — Key Technical Decisions section (cite exact values in ADRs)

**Files NOT to modify:**
- `.cursor/**` — submodule, never edit from here
- `LICENSE` — already exists, do not change
- `doc/project-progress/brief.md`, `spec.md`, `roadmap.md`, `GLOSSARY.md` — already final

**Interfaces from prior Tasks:** none (this is the first Task)

## Dependencies

None.

## Test Specification

Tests live in `tests/skeleton/test_t010.sh` (POSIX shell, `set -euo pipefail`, executable). The script:

- **Happy path:** every required file and directory exists.
- **Edge case 1 (`.gitignore` content):** `.gitignore` contains the literal lines `__pycache__`, `node_modules`, `.env`, `nogit_data/`, `dist/`, `.mypy_cache`, `.ruff_cache` (one per check; grep with `-Fxq`).
- **Edge case 2 (ADR structure):** each ADR contains `## Context`, `## Decision`, `## Consequences`, and `**Status**: Accepted`.
- **Run command:** `bash tests/skeleton/test_t010.sh`
- **Expected exit code:** `0` (any non-zero indicates a missing or malformed artifact).

## Definition of Done

See `dod.md`. Summary:
- [ ] All directories listed in *Outputs* exist (with `.gitkeep` where empty)
- [ ] `.gitignore` covers every required category
- [ ] Root `README.md` final and proof-readable
- [ ] ADR-001 (PostgreSQL) and ADR-002 (Ethics) complete with required sections
- [ ] `tests/skeleton/test_t010.sh` passes
- [ ] Full test suite passes (no regressions)

## Recommended Coder Model

Composer-2.

## Notes

ADR-002 (Ethics framework) **must include**:
- Mission alignment (the project educates against manipulation; hence we refuse to enable it)
- An explicit "We will not sell to" list: manipulative-marketing agencies, dark-pattern designers, political microtargeting firms, gambling operators
- A "We are open to" list: HR/L&D departments, financial advisors training against bias, healthcare informed-decision tooling, judiciary training, education sector
- Process for adding categories later (a new ADR amending ADR-002, not silent edit)
