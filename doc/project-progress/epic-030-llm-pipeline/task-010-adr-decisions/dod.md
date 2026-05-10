---
apm_category: task-dod
apm_ref: E030.T010
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T010 — ADR-003 + ADR-004

## ADR documents

- [ ] `doc/architecture/decisions/ADR-003-llm-provider.md` exists with all required sections
- [ ] `doc/architecture/decisions/ADR-004-embedding-model.md` exists with all required sections
- [ ] Both ADRs use the standard format (Status, Date, Epic, Context, Decision, Rationale, Consequences)

## Dependencies

- [ ] `backend/pyproject.toml` — `openai>=1.30.0` added to `[project.dependencies]`
- [ ] `.env.example` — `OPENAI_API_KEY=` present with explanatory comment
- [ ] `pip install -e "./backend[dev]"` succeeds (run in Docker or CI equivalent)

## Quality

- [ ] No secrets committed (`.env.example` has empty value for `OPENAI_API_KEY`)
- [ ] `ruff check . && ruff format --check .` — clean (no Python files changed, but verify)

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes in this `dod.md` reflect actual state (not pre-emptively marked)
