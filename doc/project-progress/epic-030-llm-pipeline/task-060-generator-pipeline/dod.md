---
apm_category: task-dod
apm_ref: E030.T060
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T060 — Case Generator Pipeline + API Endpoint

## Generator

- [ ] `backend/src/case_gen/generator.py` — `GenerationResult` dataclass and `CaseGenerator` class exist
- [ ] `CaseGenerator.generate()` executes all 8 steps in the correct order
- [ ] Duplicate rejection: `DeduplicationService.is_duplicate()` → no DB write, `rejected=True`
- [ ] Judge fail rejection: `CaseValidator.validate().passed=False` → no DB write, `rejected=True`
- [ ] Happy path: Case + CaseTranslation + CaseEmbedding persisted in one DB transaction
- [ ] `LLMParseError` raised on missing required fields in LLM response
- [ ] `LLMTimeoutError` propagated (not caught) from `LLMClient`
- [ ] `cost_usd` populated on every `GenerationResult` (including rejected)

## API endpoint

- [ ] `backend/src/api/cases.py` — `POST /v1/cases/generate` exists
- [ ] Valid request → 201 with `GenerateResponse` JSON
- [ ] Missing `bias_type_slug` → 422
- [ ] `LLMTimeoutError` → 503 (exception handler in `main.py`)
- [ ] Router registered in `backend/src/main.py`

## Tests

- [ ] `tests/case_gen/test_generator.py` — all 5 unit tests pass
- [ ] `tests/api/test_api_cases.py` — all 3 unit tests pass
- [ ] Integration test marked `@pytest.mark.integration`, skipped when `OPENAI_API_KEY` absent
- [ ] `pytest -m "not integration" -q` — full unit suite green, no regressions

## Epic MVP gate (verify end-to-end after T060 is complete)

- [ ] `alembic upgrade head` succeeds (all 3 migrations)
- [ ] `GET /v1/health` → 200
- [ ] `POST /v1/cases/generate` with `{"bias_type_slug": "anchoring", "variant": 0}`
  returns 201 (with or without live API key — 503 is acceptable if key absent)
- [ ] Structured LLM cost log entry visible in backend logs on live generation
- [ ] `pytest -m integration -q` with `OPENAI_API_KEY` set: end-to-end test passes

## Quality

- [ ] `mypy src/ alembic/env.py --strict` — clean
- [ ] `ruff check . && ruff format --check .` — clean

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes reflect actual state (DoD integrity rule)
