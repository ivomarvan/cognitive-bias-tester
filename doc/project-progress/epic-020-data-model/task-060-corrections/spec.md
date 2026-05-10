---
apm_category: task-spec
apm_ref: E020.T060
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T060 — Corrections & DoD Integrity Fix

## Goal

Fix four quality issues discovered during the E020 epic review:
1. Three missing `report.md` files (T010, T020, T030) — DoD marked ✅ but files don't exist.
2. `correct_option` is always `1` in all 25 seed cases — unrealistic, reduces dataset quality.
3. `Integer` vs `SmallInteger` discrepancy between `plan.md` and implementation — document decision.
4. `mypy` CI job does not cover `alembic/env.py`, but skeleton test and DoD T010 reference it — align.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-020-data-model/plan.md`
- `doc/project-progress/epic-020-data-model/task-010-domain-models/spec.md`
- `doc/project-progress/epic-020-data-model/task-020-repository-layer/spec.md`
- `doc/project-progress/epic-020-data-model/task-030-seed-data/spec.md`
- `.cursor/skills/execute-task/SKILL.md` — see report template and Odchylky section
- `.cursor/rules/07-project-management.mdc`

### Files to modify
- `doc/project-progress/epic-020-data-model/task-010-domain-models/dod.md`
- `doc/project-progress/epic-020-data-model/task-020-repository-layer/dod.md`
- `doc/project-progress/epic-020-data-model/task-030-seed-data/dod.md`
- `backend/src/db/seed/cases.json`
- `.github/workflows/ci.yml`

### Files to create
- `doc/project-progress/epic-020-data-model/task-010-domain-models/report.md`
- `doc/project-progress/epic-020-data-model/task-020-repository-layer/report.md`
- `doc/project-progress/epic-020-data-model/task-030-seed-data/report.md`
- `doc/project-progress/epic-020-data-model/task-060-corrections/report.md`

### APM Output
Coder **must** write `doc/project-progress/epic-020-data-model/task-060-corrections/report.md`
and fill `task-060-corrections/dod.md`. These are in Coder's own task directory and are
explicitly required — the "Files to modify" constraint does NOT restrict them.

## Sub-tasks

### 1. Write retrospective report.md for T010, T020, T030

For each of the three tasks, create `report.md` using the standard template
(see `execute-task/SKILL.md` § Step 6). The report is retrospective — describe
what was actually implemented, not what was planned.

Required sections for each report:
- `## Co bylo implementováno` — brief description of actual implementation
- `## Vstupy a výstupy` — files read / created / changed
- `## Použité metody a rozhodnutí` — key decisions
- `## Odchylky od spec.md` — T010 must document Integer vs SmallInteger (see below)
- `## Reference do kódu` — file:line references to key implemented code
- `## Výsledek regresního testu` — reference the CI run or local run result
- `## Definition of Done` — link to dod.md

After writing each `report.md`, update the corresponding `dod.md` so that
the "report.md exists" checkbox actually reflects reality (mark ✅ only if
the file now exists on disk).

### 2. Fix correct_option distribution in cases.json

All 25 cases in `backend/src/db/seed/cases.json` currently have `correct_option: 1`.
Redistribute so the correct answer appears at each index (0, 1, 2, 3) roughly equally.

Rules:
- 25 cases → target distribution: indices 0–3, approximately 6–7 per index.
- When changing `correct_option` for a case, also **reorder the `options` array** so
  that the **semantically correct answer** (the rational/unbiased choice) moves to
  the new index position. Do NOT change the text of any answer — only reorder
  the options array and update `correct_option` accordingly.
- Resulting distribution must have at least 4 cases per index (0, 1, 2, 3).
- Re-run seed after the change and verify with integration test.

### 3. Document Integer vs SmallInteger (T010 report § Odchylky od spec.md)

In the T010 retrospective report, add to `§ Odchylky od spec.md`:
```
- Column types: plan.md specifies SmallInteger for bias_type.id and
  case.bias_type_id; implementation uses Integer.
  Reason: SQLAlchemy's Integer maps to PostgreSQL INTEGER which is sufficient
  for the expected row count (< 100 bias types). SmallInteger would require
  a migration change if the table grew beyond 32 767 rows — unlikely, but
  Integer avoids that risk with negligible storage overhead.
  Decision: keep Integer; plan.md reflects an early draft constraint.
```

No code change required for this item.

### 4. Align mypy CI with DoD / skeleton tests

Currently `ci.yml` runs `mypy src/ --strict` but `tests/skeleton/test_t040.sh`
and `task-010-domain-models/dod.md` reference `alembic/env.py`.

Fix: update `ci.yml` to:
```yaml
- name: Mypy (strict)
  working-directory: backend
  run: mypy src/ alembic/env.py --strict
```

Then verify `alembic/env.py` passes mypy strict (fix any type issues if found).

## Test Specification

- No new unit tests required; all existing tests must still pass.
- After fixing `cases.json`, run the seed script in Docker and verify
  `GET /v1/i18n/en` still returns 200 (seed idempotency check).
- Verify `mypy src/ alembic/env.py --strict` passes in Docker.
- Run `pytest -m "not integration" -q` — all unit tests green.

## Definition of Done

See `dod.md` in this directory.
