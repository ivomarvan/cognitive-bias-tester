---
apm_category: task-dod
apm_ref: E020.T060
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T060 — Corrections & DoD Integrity Fix

## Retrospective reports (T010, T020, T030)

- [x] ✅ `task-010-domain-models/report.md` exists with all required sections
- [x] ✅ `task-020-repository-layer/report.md` exists with all required sections
- [x] ✅ `task-030-seed-data/report.md` exists with all required sections
- [x] ✅ Each report includes `## Odchylky od spec.md` section (even if `—`)
- [x] ✅ `task-010-domain-models/dod.md` — "report.md exists" checkbox matches reality
- [x] ✅ `task-020-repository-layer/dod.md` — "report.md exists" checkbox matches reality
- [x] ✅ `task-030-seed-data/dod.md` — "report.md exists" checkbox matches reality

## Seed data — correct_option diversity

- [x] ✅ `cases.json` — `correct_option` is no longer uniform; at least 4 values per index (0–3)
- [x] ✅ Options arrays are reordered to match new `correct_option` index (no answer text changed)
- [x] ✅ Seed script runs idempotently after the change (no crash, no duplicate key error)
- [x] ✅ `GET /v1/i18n/en` returns 200 after re-seed (smoke check that DB + seed still work)

## Integer vs SmallInteger documentation

- [x] ✅ T010 `report.md § Odchylky od spec.md` documents the Integer vs SmallInteger decision with rationale

## mypy / CI alignment

- [x] ✅ `ci.yml` mypy step runs `mypy src/ alembic/env.py --strict`
- [x] ✅ `mypy src/ alembic/env.py --strict` passes in Docker without errors

## Quality gates

- [x] ✅ `pytest -m "not integration" -q` — all unit tests pass (no regressions)
- [x] ✅ `ruff check . && ruff format --check .` — clean
- [x] ✅ This task's `report.md` written with all required sections

---

**Filled by Coder:** Composer, 2026-05-10
