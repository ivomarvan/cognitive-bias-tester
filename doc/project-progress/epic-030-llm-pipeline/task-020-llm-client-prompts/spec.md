---
apm_category: task-spec
apm_ref: E030.T020
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T020 — LLM Client + Prompt Templates

## Goal

Implement the OpenAI chat-completion client with structured cost tracking, and the
versioned prompt templates for Case generation and LLM-as-judge validation.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md` — Cross-Task Conventions, T020 scope
- `doc/architecture/decisions/ADR-003-llm-provider.md` (T010 output)
- `backend/src/core/config.py` — Settings pattern
- `backend/src/core/logging.py` — structured logging pattern
- `backend/src/db/models/case.py`, `backend/src/db/models/case_translation.py` — Case schema

### Files to create
- `backend/src/llm/__init__.py`
- `backend/src/llm/client.py`
- `backend/src/llm/exceptions.py`
- `backend/src/prompts/__init__.py`
- `backend/src/prompts/_meta.py`
- `backend/src/prompts/case_generator.py`
- `backend/src/prompts/case_validator.py`
- `backend/tests/fixtures/llm/generate_case_anchoring.json`
- `backend/tests/fixtures/llm/generate_case_framing.json`
- `backend/tests/fixtures/llm/validate_case_pass.json`
- `backend/tests/fixtures/llm/validate_case_fail.json`
- `backend/tests/llm/test_llm_client.py`
- `backend/tests/llm/test_prompts.py`
- `backend/tests/llm/__init__.py`

### Files to modify
- `backend/src/core/config.py` — add `OPENAI_API_KEY`, `LLM_MODEL`, `LLM_TIMEOUT_S`,
  `LLM_MAX_RETRIES` settings

### APM Output
Coder MUST write `doc/project-progress/epic-030-llm-pipeline/task-020-llm-client-prompts/report.md`
and fill `task-020-llm-client-prompts/dod.md`.

## Implementation Spec

### `backend/src/llm/exceptions.py`

```python
class LLMError(Exception): ...
class LLMTimeoutError(LLMError): ...
class LLMParseError(LLMError): ...   # response not parseable as expected JSON
```

### `backend/src/llm/client.py`

```python
class LLMClient:
    """OpenAI chat-completion client with structured cost logging."""

    def __init__(self, settings: Settings) -> None: ...

    async def generate_chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,          # defaults to settings.LLM_MODEL
        response_format: dict | None = None,
    ) -> str:
        """Call OpenAI chat completions; return content string.

        Raises:
            LLMTimeoutError: if request exceeds settings.LLM_TIMEOUT_S.
            LLMError: on any other API error after max retries.
        """
        ...
```

Cost logging — after each successful call:
```python
logger.info(
    "llm.call",
    model=model,
    prompt_tokens=usage.prompt_tokens,
    completion_tokens=usage.completion_tokens,
    estimated_cost_usd=round(_estimate_cost(model, usage), 6),
)
```

Cost estimation helper (private):
```python
# Prices in USD per 1M tokens (update when OpenAI changes pricing)
_COST_PER_1M = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
}
```

### `backend/src/prompts/_meta.py`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PromptMeta:
    name: str
    version: str   # semver string, e.g. "1.0.0"
```

### `backend/src/prompts/case_generator.py`

`CASE_GEN_PROMPT = PromptMeta(name="case_generator", version="1.0.0")`

System prompt must:
- instruct the model to act as a cognitive-bias scenario designer
- specify output format as JSON object matching the schema below
- prohibit markdown fences or extra commentary in the output

Required JSON schema (embed in system prompt):
```json
{
  "title": "string — short scenario title (≤10 words)",
  "question": "string — scenario + question, may contain {placeholder} tokens",
  "options": [
    {"label": "A", "text": "string, may contain {placeholder} tokens"},
    {"label": "B", "text": "..."},
    {"label": "C", "text": "..."},
    {"label": "D", "text": "..."}
  ],
  "correct_option": "integer 0–3 (index into options array)",
  "explanation": "string — why the correct option avoids the bias",
  "parametric_payload": {"key": "example_value"}
}
```

User prompt must include:
- bias type name and slug
- variant number (hint: produce a scenario different from previous variants)
- instruction to vary `correct_option` index (not always 0 or 1)

`build_user_prompt(bias_type: str, variant: int, parametric_keys: list[str]) -> str`

### `backend/src/prompts/case_validator.py`

`CASE_VALIDATOR_PROMPT = PromptMeta(name="case_validator", version="1.0.0")`

System prompt: instruct model to evaluate whether the provided Case correctly
demonstrates the target cognitive bias.

Required output JSON schema:
```json
{
  "pass": "boolean",
  "score": "float 0.0–1.0",
  "reasoning": "string ≤200 chars"
}
```

`build_user_prompt(case_json: str, target_bias: str) -> str`

### Settings additions in `backend/src/core/config.py`

```python
OPENAI_API_KEY: str          # required; no default
LLM_MODEL: str = "gpt-4o-mini"
LLM_TIMEOUT_S: int = 30
LLM_MAX_RETRIES: int = 3
```

Since `OPENAI_API_KEY` is now required, update `backend/tests/conftest.py` to also set
`os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used-in-unit-tests")`.

### CI test fixtures

Create minimal but valid recorded responses in `backend/tests/fixtures/llm/`:

`generate_case_anchoring.json` — simulates a successful `chat.completions.create` response:
```json
{
  "id": "chatcmpl-test",
  "object": "chat.completion",
  "model": "gpt-4o-mini",
  "choices": [{"message": {"role": "assistant", "content": "{\"title\":\"The car lot\",\"question\":\"...\",\"options\":[{\"label\":\"A\",\"text\":\"...\"},{\"label\":\"B\",\"text\":\"...\"},{\"label\":\"C\",\"text\":\"...\"},{\"label\":\"D\",\"text\":\"...\"}],\"correct_option\":2,\"explanation\":\"...\",\"parametric_payload\":{\"name\":\"Alex\"}}"}, "finish_reason": "stop", "index": 0}],
  "usage": {"prompt_tokens": 350, "completion_tokens": 180, "total_tokens": 530}
}
```

`validate_case_pass.json` — judge passes:
content field: `{"pass": true, "score": 0.85, "reasoning": "Case correctly frames anchoring."}`

`validate_case_fail.json` — judge fails:
content field: `{"pass": false, "score": 0.3, "reasoning": "Scenario does not demonstrate anchoring."}`

## Test Specification

### `tests/llm/test_llm_client.py`
- mock `openai.AsyncOpenAI` to return fixture response → verify returned content string
- verify cost log entry emitted with correct token counts
- mock timeout → verify `LLMTimeoutError` raised

### `tests/llm/test_prompts.py`
- `build_system_prompt()` for case_generator → non-empty, contains "JSON"
- `build_user_prompt("anchoring", 0, [])` → non-empty, contains "anchoring"
- `build_user_prompt` for all 5 bias types → non-empty (parametrised test)
- validator `build_system_prompt()` → contains "pass", "score", "reasoning"

## Definition of Done

See `dod.md` in this directory.
