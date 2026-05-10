---
apm_category: epic-plan
apm_ref: E030
apm_level: epic
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder, Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Epic Plan: E030 — LLM Pipeline & Cache

## Epic Goal

Implement the complete LLM generation pipeline: a versioned prompt layer, an OpenAI
client with cost tracking, embedding-based deduplication, an LLM-as-judge validator,
a DB-backed cyclic buffer (replacing the E020 stub), and the end-to-end Case generator
service. After this Epic, the system can autonomously produce, validate, deduplicate, and
store new Cases without human authorship.

---

## ⚠ Provider Decisions — Human Sign-off Required Before T010

The following decisions are proposed by the Planner. **Human must approve (or override)
before Coder begins T010.** The rest of the Epic plan assumes these choices.

### ADR-003 — LLM Provider: OpenAI GPT-4o-mini

| Provider | Quality | Price (in/out per 1M tokens) | Python SDK | Verdict |
|---|---|---|---|---|
| OpenAI GPT-4o-mini | ★★★★☆ | $0.15 / $0.60 | `openai` ≥ 1.0, excellent | **Recommended** |
| Anthropic Claude 3.5 Haiku | ★★★★☆ | $0.80 / $4.00 | `anthropic`, good | Pricier, no advantage for MVP |
| Google Gemini 2.0 Flash | ★★★☆☆ | $0.075 / $0.30 | `google-genai`, less mature | Cheaper but lower reliability |

**Recommendation: OpenAI GPT-4o-mini.**

Rationale: best cost/quality trade-off for structured JSON generation; mature SDK with
typed responses; excellent support for `response_format=json`; widely documented patterns
for bias-quiz use cases. Cost per Case (generation + judge call, ~1 500 tokens total):
≈ $0.001. At 10 000 Cases/month: ≈ $10/month — well within solo-developer budget.

### ADR-004 — Embedding Model: OpenAI text-embedding-3-small

| Option | Quality | Cost | Infrastructure | Verdict |
|---|---|---|---|---|
| OpenAI text-embedding-3-small | ★★★★☆ | $0.02/1M tokens | None (already using OpenAI) | **Recommended** |
| sentence-transformers (local) | ★★★★☆ | $0 per call | +400 MB Docker image, torch | Overkill for MVP scale |
| OpenAI text-embedding-3-large | ★★★★★ | $0.13/1M tokens | None | Over-engineered for <1 000 cases |

**Recommendation: OpenAI text-embedding-3-small.**

Rationale: piggybacks on the OpenAI dependency from ADR-003; negligible cost (25 seed
Cases + buffer of ~200 cases → < $0.01 total); no additional Docker infrastructure.

**Storage**: PostgreSQL `FLOAT8[]` column (no pgvector extension needed for MVP with
< 1 000 Cases). Cosine similarity computed in Python. If post-MVP scale requires pgvector,
migration is straightforward.

**New env var required**: `OPENAI_API_KEY` in `.env` and `.env.example`.

---

## Task List

| Task | Name | Depends on | Parallel with | Coder model |
|------|------|-----------|---------------|-------------|
| T010 | ADR-003 + ADR-004 Docs | (Human approval) | — | Composer-2 |
| T020 | LLM Client + Prompt Templates | T010 | T050 | Composer-2 |
| T030 | Embedding Client + Deduplication | T020 | T040 | Composer-2 |
| T040 | LLM-as-Judge Validator | T020 | T030 | Composer-2 |
| T050 | DB-backed Cyclic Buffer | T010 | T020 | Composer-2 |
| T060 | Case Generator Pipeline + API | T020, T030, T040, T050 | — | Composer-2 |

```
T010 → T020 → T030 ─┐
              T040 ─┤→ T060
T010 → T050 ────────┘
```

---

## APM Output Convention

Each task ends with:
- `report.md` in the task's own directory (Coder MUST create it — see `07-project-management.mdc`
  and `execute-task/SKILL.md` § DoD Integrity Rule)
- `dod.md` checkboxes filled (only after verifying each artifact actually exists)
- `§ Odchylky od spec.md` in every report (even if `—`)

---

## Cross-Task Conventions

### Package layout

```
backend/src/
├── llm/
│   ├── __init__.py
│   ├── client.py          # OpenAI chat client + cost tracking
│   ├── embedding.py       # OpenAI embedding client
│   └── exceptions.py      # LLMError, EmbeddingError, JudgeError
├── prompts/
│   ├── __init__.py
│   ├── _meta.py           # PromptMeta dataclass (name, version, hash)
│   ├── case_generator.py  # system + user templates for Case generation
│   └── case_validator.py  # system + user templates for judge validation
├── dedup/
│   ├── __init__.py
│   └── service.py         # cosine similarity deduplication
├── case_gen/
│   ├── __init__.py
│   ├── generator.py       # CaseGenerator orchestrator
│   └── validator.py       # CaseValidator (judge)
└── db/
    ├── models/
    │   └── case_embedding.py  # new ORM model
    ├── repositories/
    │   └── embedding_repository.py
    └── buffer/
        ├── __init__.py
        └── postgres_buffer.py  # PostgresCyclicBuffer
```

### Testing strategy (CI-safe — no live API calls)

All LLM and embedding calls in unit tests use **pre-recorded JSON fixtures**:
```
backend/tests/fixtures/llm/
├── generate_case_anchoring.json   # recorded OpenAI chat response
├── generate_case_framing.json
├── validate_case_pass.json        # judge response, pass
├── validate_case_fail.json        # judge response, fail
└── embed_case_01.json             # recorded embedding response
```

Integration tests (pytest.mark.integration) may use live API if `OPENAI_API_KEY`
is set; skipped in CI otherwise.

### Cost tracking

Every LLM call logs to structured log:
```python
logger.info(
    "llm.call",
    model=model,
    prompt_tokens=usage.prompt_tokens,
    completion_tokens=usage.completion_tokens,
    estimated_cost_usd=_estimate_cost(model, usage),
)
```

---

## T010 — ADR-003 + ADR-004: Architecture Decision Records

**Goal:** Commit the two ADRs documenting the provider choices approved in this plan.

**Scope:**
- Create `doc/architecture/decisions/ADR-003-llm-provider.md`
- Create `doc/architecture/decisions/ADR-004-embedding-model.md`
- Add `OPENAI_API_KEY=` to `.env.example`
- Add `openai>=1.30.0` to `backend/pyproject.toml` (base dependencies)

**No backend code changes in this task** — pure documentation + dependency declaration.

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md` (Provider Decisions section)
- Read: `doc/architecture/decisions/ADR-001-use-postgresql.md` (format reference)
- Do NOT modify: any `src/` files
- Do NOT modify: `doc/**` except — Coder MUST write `task-010-adr-decisions/report.md`
  and fill `task-010-adr-decisions/dod.md`

**Recommended Coder model:** Composer-2

---

## T020 — LLM Client + Prompt Templates

**Goal:** Implement the OpenAI chat completion client with cost tracking, and the versioned
prompt templates for Case generation and judge validation.

**Scope:**
- `backend/src/llm/client.py` — `LLMClient` class (sync wrapper around `openai.AsyncOpenAI`)
  - `generate_chat(messages, model, response_format) -> str`
  - internal cost tracking: log every call with token counts + estimated USD cost
  - configurable timeout and max retries (from `settings`)
- `backend/src/llm/exceptions.py` — `LLMError(Exception)`, `LLMTimeoutError`
- `backend/src/prompts/_meta.py` — `PromptMeta(name: str, version: str)`
- `backend/src/prompts/case_generator.py` — `CASE_GEN_PROMPT: PromptMeta`
  - `build_system_prompt() -> str`
  - `build_user_prompt(bias_type: str, variant: int, parametric_keys: list[str]) -> str`
  - Output schema embedded in system prompt (JSON with title, question, options[4],
    correct_option, explanation, parametric_payload)
- `backend/src/prompts/case_validator.py` — `CASE_VALIDATOR_PROMPT: PromptMeta`
  - `build_system_prompt() -> str`
  - `build_user_prompt(case_json: str, target_bias: str) -> str`
  - Output schema: `{pass: bool, score: float, reasoning: str}`

**Settings additions:**
```python
OPENAI_API_KEY: str
LLM_MODEL: str = "gpt-4o-mini"
LLM_TIMEOUT_S: int = 30
LLM_MAX_RETRIES: int = 3
```

**CI test fixtures:** create `tests/fixtures/llm/` with ≥ 3 recorded chat responses.

**Unit tests:**
- `test_llm_client.py` — mock `openai.AsyncOpenAI`, verify cost logging
- `test_prompts.py` — verify prompt templates produce valid non-empty strings
  for each bias type; verify JSON schema embedded in system prompt is parseable

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md` (Cross-Task Conventions)
- Read: `backend/src/core/config.py` (Settings pattern)
- Read: `backend/src/core/logging.py` (structured logging pattern)
- Read: `backend/src/db/models/case.py` (Case structure reference)
- Do NOT modify: existing db/, api/ code
- Do NOT modify: `doc/**` except Coder MUST write `task-020-llm-client-prompts/report.md`
  and fill `task-020-llm-client-prompts/dod.md`

**Recommended Coder model:** Composer-2

---

## T030 — Embedding Client + Deduplication Service

**Goal:** Implement the OpenAI embedding client, store embeddings in PostgreSQL, and
provide cosine-similarity-based deduplication as a service.

**Scope:**
- New ORM model `backend/src/db/models/case_embedding.py`:
  ```python
  class CaseEmbedding(Base):
      case_id: Mapped[uuid.UUID]  # FK → case.id ON DELETE CASCADE
      model: Mapped[str]           # e.g. "text-embedding-3-small"
      vector: Mapped[list[float]]  # FLOAT8[]
      created_at: Mapped[datetime]
  ```
- Alembic migration `0003_add_case_embedding`
- `backend/src/db/repositories/embedding_repository.py` — `EmbeddingRepository`:
  - `upsert(case_id, model, vector) -> None`
  - `get_all_vectors(model) -> list[tuple[uuid.UUID, list[float]]]`
- `backend/src/llm/embedding.py` — `EmbeddingClient`:
  - `embed(text: str, model: str = "text-embedding-3-small") -> list[float]`
  - uses `openai.AsyncOpenAI().embeddings.create()`
- `backend/src/dedup/service.py` — `DeduplicationService`:
  - `is_duplicate(candidate_vector, existing_vectors, threshold: float = 0.92) -> bool`
  - cosine similarity computed with `numpy` or plain Python (no numpy if not already dep)
  - `DEDUP_THRESHOLD: float = 0.92` configurable via settings

**Settings additions:**
```python
EMBEDDING_MODEL: str = "text-embedding-3-small"
DEDUP_THRESHOLD: float = 0.92
```

**CI test fixtures:** `tests/fixtures/llm/embed_*.json` with pre-computed vectors.

**Unit tests:**
- `test_embedding_client.py` — mock `openai.AsyncOpenAI.embeddings`, verify fixture loading
- `test_dedup_service.py` — verify cosine similarity logic with hand-computed vectors;
  test edge cases (identical vectors → duplicate, orthogonal → not duplicate)
- `test_embedding_repository.py` — unit test with SQLAlchemy in-memory or mock

**Depends on:** T020 (for `LLMClient` patterns and OpenAI SDK setup)

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md`
- Read: `backend/src/llm/client.py`, `backend/src/llm/exceptions.py` (T020 output)
- Read: `backend/src/db/models/case.py`, `backend/src/db/base.py`
- Read: `backend/alembic/versions/0002_domain_model.py` (migration pattern)
- Do NOT modify: `doc/**` except Coder MUST write `task-030-embedding-dedup/report.md`
  and fill `task-030-embedding-dedup/dod.md`

**Recommended Coder model:** Composer-2

---

## T040 — LLM-as-Judge Validator

**Goal:** Implement the `CaseValidator` service that calls the LLM judge prompt and
returns a structured validation result.

**Scope:**
- `backend/src/case_gen/validator.py` — `CaseValidator`:
  ```python
  @dataclass
  class ValidationResult:
      passed: bool
      score: float       # 0.0–1.0
      reasoning: str

  class CaseValidator:
      async def validate(self, case_json: str, bias_type_slug: str) -> ValidationResult
  ```
  - calls `LLMClient.generate_chat()` with judge prompt from T020
  - parses JSON response `{pass: bool, score: float, reasoning: str}`
  - raises `JudgeError` if response is malformed or unparseable
- `backend/src/llm/exceptions.py` — add `JudgeError`

**Unit tests:**
- `test_case_validator.py`:
  - fixture `validate_case_pass.json` → `ValidationResult(passed=True, score≥0.7)`
  - fixture `validate_case_fail.json` → `ValidationResult(passed=False, score<0.5)`
  - malformed JSON response → `JudgeError` raised
  - correct bias_type_slug passed in user prompt (assert via mock capture)

**Depends on:** T020 (LLMClient + validator prompt templates)

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md`
- Read: `backend/src/llm/client.py`, `backend/src/prompts/case_validator.py` (T020 output)
- Do NOT modify: existing db/, api/ code
- Do NOT modify: `doc/**` except Coder MUST write `task-040-judge-validator/report.md`
  and fill `task-040-judge-validator/dod.md`

**Recommended Coder model:** Composer-2

---

## T050 — DB-backed Cyclic Buffer

**Goal:** Replace `InMemoryCyclicBuffer` from E020 with `PostgresCyclicBuffer` — a
production-ready implementation backed by the `case` table, with composite eviction.

**Scope:**
- `backend/src/db/buffer/postgres_buffer.py` — `PostgresCyclicBuffer`:
  - implements `CyclicBuffer` protocol from `backend/src/db/buffer/interface.py` (E020/T050)
  - `capacity: int` configurable via `settings.BUFFER_CAPACITY`
  - `get_next() -> Case | None` — round-robin by `(created_at ASC)` among active cases
  - `insert(case: Case) -> bool` — insert; if at capacity evict worst before inserting
  - `should_generate() -> bool` — True if `count(active) < capacity * BUFFER_REFILL_THRESHOLD`
  - **Eviction query**: `SELECT id FROM case WHERE status='active' ORDER BY
    CASE WHEN rating_count = 0 THEN 0.0 ELSE rating_sum::float/rating_count END ASC,
    created_at ASC LIMIT 1`
  - sets evicted Case `status='evicted'`

**Settings additions:**
```python
BUFFER_CAPACITY: int = 100
BUFFER_REFILL_THRESHOLD: float = 0.8   # generate when buffer < 80% full
```

**Unit tests:**
- `test_postgres_buffer.py`:
  - `should_generate()` returns True when count < capacity * threshold
  - `insert()` at capacity triggers eviction of correct Case (mock DB query)
  - eviction selects lowest `rating_avg` Case (verify ORDER BY via mock)
- Integration test (`@pytest.mark.integration`):
  - full round-trip: insert 3 Cases → evict → verify evicted Case status = 'evicted'

**Depends on:** T010 (settings pattern); can run in parallel with T020.

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md`
- Read: `backend/src/db/buffer/interface.py` (E020/T050 — CyclicBuffer protocol)
- Read: `backend/src/db/models/case.py`, `backend/src/db/repositories/` (E020)
- Read: `backend/src/core/config.py` (Settings pattern)
- Do NOT modify: `backend/src/db/buffer/interface.py` (protocol is frozen)
- Do NOT modify: `doc/**` except Coder MUST write `task-050-cyclic-buffer-db/report.md`
  and fill `task-050-cyclic-buffer-db/dod.md`

**Recommended Coder model:** Composer-2

---

## T060 — Case Generator Pipeline + API Endpoint

**Goal:** Wire T020–T050 into the end-to-end `CaseGenerator` service and expose it via
`POST /v1/cases/generate`.

**Scope:**
- `backend/src/case_gen/generator.py` — `CaseGenerator`:
  ```python
  @dataclass
  class GenerationResult:
      case: Case | None          # None if rejected
      rejected: bool
      rejection_reason: str | None   # "duplicate" | "judge_fail" | None
      validation: ValidationResult | None
      cost_usd: float

  class CaseGenerator:
      async def generate(self, bias_type_slug: str, variant: int) -> GenerationResult
  ```
  Steps:
  1. Build user prompt for `(bias_type_slug, variant)`
  2. Call `LLMClient` → raw JSON string
  3. Parse → `CaseTranslation` + `Case` ORM objects (English locale)
  4. Call `EmbeddingClient` → vector
  5. Call `DeduplicationService.is_duplicate()` → if True return rejected result
  6. Call `CaseValidator.validate()` → if not passed return rejected result
  7. Persist `Case` + `CaseTranslation` + `CaseEmbedding` in DB (one transaction)
  8. Return `GenerationResult(case=case, ...)`
- `backend/src/api/cases.py` — new router:
  ```
  POST /v1/cases/generate
  Body: {"bias_type_slug": str, "variant": int}
  Response 201: GenerationResult (camelCase JSON)
  Response 422: validation error
  Response 503: LLM unavailable
  ```
- Register router in `main.py`

**Unit tests:**
- `test_generator.py`:
  - happy path: LLM returns valid JSON → judge passes → not duplicate → Case stored
  - duplicate rejection: `DeduplicationService` returns True → `GenerationResult(rejected=True, ...)`
  - judge fail: validator returns `passed=False` → rejected
  - LLM timeout: `LLMTimeoutError` → propagated cleanly
- `test_api_cases.py`: HTTP-level test via ASGITransport (no lifespan):
  - POST with valid body → 201
  - POST with missing `bias_type_slug` → 422

**Integration test** (`@pytest.mark.integration`):
  - End-to-end with `OPENAI_API_KEY` set: generate one Case for `anchoring` variant 0;
    assert it is stored in DB and returned. Skip if API key not set.

**Depends on:** T020 (LLMClient, prompts), T030 (EmbeddingClient, DeduplicationService),
T040 (CaseValidator), T050 (PostgresCyclicBuffer via buffer check)

**Context Bundle:**
- Read: `doc/project-progress/epic-030-llm-pipeline/plan.md` (full spec above)
- Read: T020 output: `backend/src/llm/`, `backend/src/prompts/`
- Read: T030 output: `backend/src/llm/embedding.py`, `backend/src/dedup/service.py`
- Read: T040 output: `backend/src/case_gen/validator.py`
- Read: T050 output: `backend/src/db/buffer/postgres_buffer.py`
- Read: `backend/src/db/repositories/` (E020 — for DB persistence)
- Read: `backend/src/api/health.py` (router pattern)
- Do NOT modify: existing models, migrations, or repositories
- Do NOT modify: `doc/**` except Coder MUST write `task-060-generator-pipeline/report.md`
  and fill `task-060-generator-pipeline/dod.md`

**Recommended Coder model:** Composer-2
