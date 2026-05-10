---
apm_category: task-dod
apm_ref: E030.T020
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T020 — LLM Client + Prompt Templates

## Implementation

- [ ] `backend/src/llm/client.py` — `LLMClient` class exists with `generate_chat()` method
- [ ] `backend/src/llm/exceptions.py` — `LLMError`, `LLMTimeoutError`, `LLMParseError` defined
- [ ] `backend/src/prompts/_meta.py` — `PromptMeta` dataclass defined
- [ ] `backend/src/prompts/case_generator.py` — `CASE_GEN_PROMPT`, `build_system_prompt()`,
  `build_user_prompt()` implemented
- [ ] `backend/src/prompts/case_validator.py` — `CASE_VALIDATOR_PROMPT`, both build functions

## Settings

- [ ] `backend/src/core/config.py` — `OPENAI_API_KEY`, `LLM_MODEL`, `LLM_TIMEOUT_S`,
  `LLM_MAX_RETRIES` added to `Settings`
- [ ] `backend/tests/conftest.py` — `OPENAI_API_KEY` set to a dummy value for unit tests

## Cost tracking

- [ ] Every `LLMClient.generate_chat()` call emits a structured `llm.call` log entry with
  `model`, `prompt_tokens`, `completion_tokens`, `estimated_cost_usd`

## Fixtures

- [ ] `backend/tests/fixtures/llm/generate_case_anchoring.json` exists
- [ ] `backend/tests/fixtures/llm/generate_case_framing.json` exists
- [ ] `backend/tests/fixtures/llm/validate_case_pass.json` exists
- [ ] `backend/tests/fixtures/llm/validate_case_fail.json` exists

## Tests

- [ ] `tests/llm/test_llm_client.py` — all tests pass (mock OpenAI client)
- [ ] `tests/llm/test_prompts.py` — all tests pass
- [ ] `pytest -m "not integration" -q` — full unit suite green, no regressions

## Quality

- [ ] `mypy src/ alembic/env.py --strict` — clean
- [ ] `ruff check . && ruff format --check .` — clean

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes reflect actual state (DoD integrity rule)
