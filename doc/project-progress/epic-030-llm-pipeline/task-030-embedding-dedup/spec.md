---
apm_category: task-spec
apm_ref: E030.T030
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T030 — Embedding Client + Deduplication Service

## Goal

Implement the OpenAI embedding client, a new `case_embedding` DB table, and a
cosine-similarity deduplication service that rejects near-duplicate Cases before
they enter the cyclic buffer.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md`
- `doc/architecture/decisions/ADR-004-embedding-model.md` (T010 output)
- `backend/src/llm/client.py`, `backend/src/llm/exceptions.py` (T020 output)
- `backend/src/db/models/case.py`, `backend/src/db/base.py`
- `backend/alembic/versions/0002_domain_model.py` — migration format reference
- `backend/src/core/config.py` — Settings pattern

### Files to create
- `backend/src/db/models/case_embedding.py`
- `backend/src/db/repositories/embedding_repository.py`
- `backend/src/llm/embedding.py`
- `backend/src/dedup/__init__.py`
- `backend/src/dedup/service.py`
- `backend/alembic/versions/0003_add_case_embedding.py`
- `backend/tests/fixtures/llm/embed_case_01.json`
- `backend/tests/fixtures/llm/embed_case_02_near_duplicate.json`
- `backend/tests/db/test_embedding_repository.py`
- `backend/tests/llm/test_embedding_client.py`
- `backend/tests/dedup/test_dedup_service.py`
- `backend/tests/dedup/__init__.py`

### Files to modify
- `backend/src/db/models/__init__.py` — export `CaseEmbedding`
- `backend/src/core/config.py` — add `EMBEDDING_MODEL`, `DEDUP_THRESHOLD`

### APM Output
Coder MUST write `task-030-embedding-dedup/report.md` and fill `task-030-embedding-dedup/dod.md`.

## Implementation Spec

### `backend/src/db/models/case_embedding.py`

```python
class CaseEmbedding(Base):
    """Stores the embedding vector for a Case (for deduplication)."""

    __tablename__ = "case_embedding"

    case_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("case.id", ondelete="CASCADE"), primary_key=True
    )
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    vector: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
```

### Alembic migration `0003_add_case_embedding`

```python
def upgrade() -> None:
    op.create_table(
        "case_embedding",
        sa.Column("case_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("case.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("model", sa.String(64), nullable=False),
        sa.Column("vector", postgresql.ARRAY(sa.Float), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.text("now()"), nullable=False),
    )
```

### `backend/src/db/repositories/embedding_repository.py`

```python
class EmbeddingRepository:
    async def upsert(
        self, case_id: uuid.UUID, model: str, vector: list[float]
    ) -> None:
        """Insert or replace the embedding for a Case."""
        ...

    async def get_all_vectors(
        self, model: str
    ) -> list[tuple[uuid.UUID, list[float]]]:
        """Return all (case_id, vector) pairs for the given model."""
        ...
```

### `backend/src/llm/embedding.py`

```python
class EmbeddingClient:
    """OpenAI embedding client returning float vectors."""

    def __init__(self, settings: Settings) -> None: ...

    async def embed(
        self,
        text: str,
        *,
        model: str | None = None,   # defaults to settings.EMBEDDING_MODEL
    ) -> list[float]:
        """Embed text and return the vector.

        Raises:
            LLMError: on API error.
        """
        ...
```

### `backend/src/dedup/service.py`

```python
def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Pure-Python cosine similarity (no numpy dependency)."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class DeduplicationService:
    """Cosine-similarity deduplication over existing Case embeddings."""

    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def is_duplicate(
        self,
        candidate: list[float],
        existing: list[tuple[uuid.UUID, list[float]]],
    ) -> bool:
        """Return True if candidate is within threshold of any existing vector."""
        return any(
            _cosine_similarity(candidate, vec) >= self._threshold
            for _, vec in existing
        )
```

### Settings additions

```python
EMBEDDING_MODEL: str = "text-embedding-3-small"
DEDUP_THRESHOLD: float = 0.92
```

### CI test fixtures

`embed_case_01.json` — simulates `embeddings.create` response for a short text:
```json
{
  "object": "list",
  "data": [{"object": "embedding", "index": 0, "embedding": [0.1, 0.2, -0.3]}],
  "model": "text-embedding-3-small",
  "usage": {"prompt_tokens": 12, "total_tokens": 12}
}
```

`embed_case_02_near_duplicate.json` — nearly identical vector (cosine sim > 0.92):
embedding should be `[0.101, 0.201, -0.299]` (same direction, slightly scaled).

## Test Specification

### `tests/llm/test_embedding_client.py`
- mock `openai.AsyncOpenAI.embeddings.create` with fixture → verify vector returned
- verify vector length matches `text-embedding-3-small` dimensions (1 536 in prod,
  3 in fixture — accept any list[float])

### `tests/dedup/test_dedup_service.py`
- identical vectors → `is_duplicate = True` (similarity = 1.0)
- orthogonal vectors `[1,0,0]` vs `[0,1,0]` → `is_duplicate = False`
- `embed_case_02_near_duplicate` vs `embed_case_01` at threshold 0.92 → `True`
- zero vector (edge case) → no crash, returns `False`

### `tests/db/test_embedding_repository.py`
- unit test with SQLAlchemy mock (async mock session)
- `upsert` then `get_all_vectors` returns inserted record

### Integration test (`@pytest.mark.integration`)
- `alembic upgrade head` creates `case_embedding` table (already covered by CI job)

## Definition of Done

See `dod.md` in this directory.
