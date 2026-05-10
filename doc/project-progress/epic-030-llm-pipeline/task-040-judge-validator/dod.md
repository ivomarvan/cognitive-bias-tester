---
apm_category: task-dod
apm_ref: E030.T040
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T040 — LLM-as-Judge Validator

## Implementation

- [ ] `backend/src/case_gen/validator.py` — `ValidationResult` dataclass and `CaseValidator` class exist
- [ ] `CaseValidator.validate()` parses `{pass, score, reasoning}` from LLM response
- [ ] `JudgeError` added to `backend/src/llm/exceptions.py`
- [ ] Malformed / missing-key JSON response → `JudgeError` raised (not crash)
- [ ] `score` out of range is clamped to `[0.0, 1.0]` without raising

## Tests

- [ ] `tests/case_gen/test_case_validator.py` — all 5 test cases pass
- [ ] pass fixture → `passed=True`, `score ≥ 0.7`
- [ ] fail fixture → `passed=False`, `score < 0.5`
- [ ] malformed JSON → `JudgeError`
- [ ] missing key → `JudgeError`
- [ ] bias_type_slug included in prompt
- [ ] `pytest -m "not integration" -q` — full unit suite green, no regressions

## Quality

- [ ] `mypy src/ alembic/env.py --strict` — clean
- [ ] `ruff check . && ruff format --check .` — clean

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes reflect actual state (DoD integrity rule)
