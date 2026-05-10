---
apm_category: task-spec
apm_ref: E030.T060
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T060 — Case Generator Pipeline + API Endpoint

## Goal

Wire T020–T050 into the end-to-end `CaseGenerator` orchestrator and expose it via
`POST /v1/cases/generate`. After this task, the system can autonomously produce,
validate, deduplicate, and store new Cases with LLM cost tracked in logs.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md` — T060 scope + API spec
- T020 output: `backend/src/llm/client.py`, `backend/src/llm/embedding.py`,
  `backend/src/prompts/case_generator.py`
- T030 output: `backend/src/dedup/service.py`,
  `backend/src/db/repositories/embedding_repository.py`
- T040 output: `backend/src/case_gen/validator.py`
- T050 output: `backend/src/db/buffer/postgres_buffer.py`
- `backend/src/db/repositories/` (E020 — `CaseRepository`, `CaseTranslationRepository`)
- `backend/src/api/health.py` — router pattern
- `backend/src/main.py` — router registration pattern

### Files to create
- `backend/src/case_gen/generator.py`
- `backend/src/api/cases.py`
- `backend/tests/case_gen/test_generator.py`
- `backend/tests/api/test_api_cases.py`

### Files to modify
- `backend/src/main.py` — register `cases` router

### APM Output
Coder MUST write `task-060-generator-pipeline/report.md` and fill `task-060-generator-pipeline/dod.md`.

## Implementation Spec

### `backend/src/case_gen/generator.py`

```python
@dataclass
class GenerationResult:
    """Result of one Case generation attempt."""

    case: Case | None                    # None when rejected
    rejected: bool
    rejection_reason: str | None         # "duplicate" | "judge_fail" | None
    validation: ValidationResult | None
    cost_usd: float                      # estimated total cost for this attempt


class CaseGenerator:
    """Orchestrates LLM call → parse → validate → deduplicate → persist."""

    def __init__(
        self,
        llm_client: LLMClient,
        embedding_client: EmbeddingClient,
        dedup_service: DeduplicationService,
        case_validator: CaseValidator,
        case_repo: CaseRepository,
        case_translation_repo: CaseTranslationRepository,
        embedding_repo: EmbeddingRepository,
    ) -> None: ...

    async def generate(
        self,
        bias_type_slug: str,
        variant: int,
    ) -> GenerationResult:
        """Generate, validate, deduplicate, and persist one Case.

        Steps:
          1. Build prompts for (bias_type_slug, variant).
          2. Call LLMClient → raw JSON string.
          3. Parse JSON → Case + CaseTranslation ORM objects (locale="en").
          4. Call EmbeddingClient → vector.
          5. Fetch existing vectors → call DeduplicationService.is_duplicate().
             If True → return GenerationResult(rejected=True, reason="duplicate").
          6. Call CaseValidator.validate() → ValidationResult.
             If not passed → return GenerationResult(rejected=True, reason="judge_fail").
          7. Persist Case + CaseTranslation + CaseEmbedding in one DB transaction.
          8. Return GenerationResult(case=case, rejected=False, validation=result, cost=...).

        Raises:
            LLMTimeoutError: propagated from LLMClient.
            LLMParseError: if LLM response is not valid JSON matching Case schema.
        """
        ...
```

Parsing the LLM response in step 3:
- Parse JSON from `generate_chat()` response
- Map to `Case` + `CaseTranslation` objects
- Required fields: title, question, options (list of 4), correct_option (0–3), explanation,
  parametric_payload
- If any required field is missing → raise `LLMParseError`
- `Case.status` = `"active"`, `Case.source` = `"llm"`
- `Case.variant` = the requested `variant` argument

### `backend/src/api/cases.py`

```python
router = APIRouter(prefix="/v1/cases", tags=["cases"])


class GenerateRequest(BaseModel):
    bias_type_slug: str
    variant: int = 0


class GenerateResponse(BaseModel):
    rejected: bool
    rejection_reason: str | None = None
    case_id: str | None = None    # UUID of stored Case, None if rejected
    score: float | None = None    # judge score
    cost_usd: float


@router.post("/generate", status_code=201, response_model=GenerateResponse)
async def generate_case(
    body: GenerateRequest,
    session: AsyncSession = Depends(get_session),
) -> GenerateResponse:
    """Generate a new Case using the LLM pipeline.

    Returns 201 with GenerateResponse regardless of acceptance/rejection.
    Returns 503 if the LLM provider is unreachable.
    """
    ...
```

Map `LLMTimeoutError` → HTTP 503 via FastAPI exception handler (add to `main.py`).

### `main.py` additions

- Import and register the `cases` router.
- Add exception handler for `LLMTimeoutError` → 503 JSON response.

## Test Specification

### `tests/case_gen/test_generator.py`

All tests mock all external services (LLMClient, EmbeddingClient, etc.):

```python
@pytest.mark.unit
async def test_generate_happy_path():
    """LLM returns valid JSON → judge passes → not duplicate → Case stored."""
    # assert GenerationResult.rejected = False, case is not None

@pytest.mark.unit
async def test_generate_duplicate_rejected():
    """DeduplicationService returns True → GenerationResult(rejected=True, reason='duplicate')."""
    # assert no DB write attempted

@pytest.mark.unit
async def test_generate_judge_fail_rejected():
    """CaseValidator returns passed=False → rejected=True, reason='judge_fail'."""

@pytest.mark.unit
async def test_generate_llm_timeout_propagates():
    """LLMClient raises LLMTimeoutError → propagated (not swallowed)."""

@pytest.mark.unit
async def test_generate_parse_error_on_bad_json():
    """LLM returns non-JSON or missing required field → LLMParseError raised."""
```

### `tests/api/test_api_cases.py`

```python
@pytest.mark.unit
async def test_post_generate_valid_body_returns_201():
    """POST /v1/cases/generate with valid body → 201."""

@pytest.mark.unit
async def test_post_generate_missing_slug_returns_422():
    """POST /v1/cases/generate without bias_type_slug → 422."""

@pytest.mark.unit
async def test_post_generate_llm_timeout_returns_503():
    """CaseGenerator raises LLMTimeoutError → HTTP 503."""
```

### Integration test (`@pytest.mark.integration`, skipped if no OPENAI_API_KEY)

```python
async def test_generate_case_end_to_end():
    """Generate one Case for anchoring variant 0 with live API.
    Assert: Case stored in DB, GenerationResult.rejected = False."""
```

## Definition of Done

See `dod.md` in this directory.
