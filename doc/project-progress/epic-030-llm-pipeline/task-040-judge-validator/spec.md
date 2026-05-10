---
apm_category: task-spec
apm_ref: E030.T040
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T040 — LLM-as-Judge Validator

## Goal

Implement `CaseValidator` — a service that calls the LLM judge prompt and returns a
structured `ValidationResult` indicating whether a newly generated Case correctly
demonstrates the target cognitive bias.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md`
- `backend/src/llm/client.py` (T020 output)
- `backend/src/llm/exceptions.py` (T020 output)
- `backend/src/prompts/case_validator.py` (T020 output)
- `backend/tests/fixtures/llm/validate_case_pass.json` (T020 output)
- `backend/tests/fixtures/llm/validate_case_fail.json` (T020 output)

### Files to create
- `backend/src/case_gen/__init__.py`
- `backend/src/case_gen/validator.py`
- `backend/tests/case_gen/__init__.py`
- `backend/tests/case_gen/test_case_validator.py`

### Files to modify
- `backend/src/llm/exceptions.py` — add `JudgeError`

### APM Output
Coder MUST write `task-040-judge-validator/report.md` and fill `task-040-judge-validator/dod.md`.

## Implementation Spec

### `backend/src/llm/exceptions.py` addition

```python
class JudgeError(LLMError):
    """Raised when the judge response cannot be parsed or is structurally invalid."""
```

### `backend/src/case_gen/validator.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Structured output from the LLM-as-judge validation step."""

    passed: bool
    score: float       # 0.0–1.0; higher = better quality
    reasoning: str     # ≤ 200 chars, human-readable


class CaseValidator:
    """Validates a generated Case against its target bias using an LLM judge."""

    def __init__(self, llm_client: LLMClient) -> None: ...

    async def validate(
        self,
        case_json: str,
        bias_type_slug: str,
    ) -> ValidationResult:
        """Call the LLM judge and parse the result.

        Args:
            case_json: JSON string of the generated Case (title, question, options, ...).
            bias_type_slug: slug of the target bias (e.g. "anchoring").

        Returns:
            ValidationResult with passed, score, reasoning.

        Raises:
            JudgeError: if the LLM response cannot be parsed as the expected JSON schema.
            LLMTimeoutError: if the judge call times out.
        """
        ...
```

Parsing logic:
- Call `LLMClient.generate_chat()` with judge prompts from `case_validator.py`
- Parse response as JSON: `{"pass": bool, "score": float, "reasoning": str}`
- If JSON parsing fails or required keys are missing → raise `JudgeError`
- If `score` is outside `[0.0, 1.0]` → clamp, not raise
- Map `pass` key (JSON boolean) → `passed` field (Python bool)

## Test Specification

### `tests/case_gen/test_case_validator.py`

```python
@pytest.mark.unit
async def test_validate_pass_fixture():
    """validate_case_pass.json fixture → ValidationResult(passed=True, score≥0.7)."""

@pytest.mark.unit
async def test_validate_fail_fixture():
    """validate_case_fail.json fixture → ValidationResult(passed=False, score<0.5)."""

@pytest.mark.unit
async def test_validate_malformed_json_raises_judge_error():
    """LLM returns non-JSON string → JudgeError raised."""

@pytest.mark.unit
async def test_validate_missing_key_raises_judge_error():
    """LLM returns JSON without 'pass' key → JudgeError raised."""

@pytest.mark.unit
async def test_validate_passes_bias_slug_to_prompt():
    """bias_type_slug is included in the user prompt sent to LLM (capture via mock)."""
```

All tests mock `LLMClient.generate_chat` — no live API calls.

## Definition of Done

See `dod.md` in this directory.
