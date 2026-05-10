---
apm_category: task-spec
apm_ref: E030.T050
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T050 — DB-backed Cyclic Buffer

## Goal

Replace the `InMemoryCyclicBuffer` stub from E020/T050 with `PostgresCyclicBuffer` —
a production-ready implementation backed by the `case` table. Eviction uses a composite
`(rating_avg ASC, created_at ASC)` ordering: the worst-rated (and, on tie, oldest) Case
is evicted first.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md`
- `backend/src/db/buffer/interface.py` (E020/T050 — `CyclicBuffer` protocol, FROZEN)
- `backend/src/db/models/case.py`
- `backend/src/db/repositories/` (E020 — patterns for async session usage)
- `backend/src/core/config.py` — Settings pattern

### Files to create
- `backend/src/db/buffer/__init__.py` (if not exists)
- `backend/src/db/buffer/postgres_buffer.py`
- `backend/tests/db/test_postgres_buffer.py`

### Files to modify
- `backend/src/core/config.py` — add `BUFFER_CAPACITY`, `BUFFER_REFILL_THRESHOLD`

### APM Output
Coder MUST write `task-050-cyclic-buffer-db/report.md` and fill `task-050-cyclic-buffer-db/dod.md`.

## Implementation Spec

### `backend/src/db/buffer/postgres_buffer.py`

```python
class PostgresCyclicBuffer:
    """Production CyclicBuffer backed by the PostgreSQL case table."""

    def __init__(self, session_factory: async_sessionmaker, settings: Settings) -> None:
        self._session_factory = session_factory
        self._capacity = settings.BUFFER_CAPACITY
        self._threshold = settings.BUFFER_REFILL_THRESHOLD

    async def get_next(self) -> Case | None:
        """Return the oldest active Case (FIFO order), or None if buffer is empty."""
        ...

    async def insert(self, case: Case) -> bool:
        """Insert Case; evict worst if at capacity. Returns True if inserted."""
        ...

    async def should_generate(self) -> bool:
        """Return True if active Case count < capacity * threshold."""
        ...

    async def _count_active(self) -> int:
        """SELECT COUNT(*) WHERE status = 'active'."""
        ...

    async def _evict_worst(self) -> None:
        """Set the worst Case to status='evicted'.

        Eviction order:
            ORDER BY
              CASE WHEN rating_count = 0 THEN 0.0
                   ELSE rating_sum::float / rating_count
              END ASC,
              created_at ASC
            LIMIT 1
        """
        ...
```

### Settings additions

```python
BUFFER_CAPACITY: int = 100
BUFFER_REFILL_THRESHOLD: float = 0.8
```

### Eviction SQL (exact expression)

```sql
SELECT id FROM "case"
WHERE status = 'active'
ORDER BY
    CASE WHEN rating_count = 0 THEN 0.0
         ELSE CAST(rating_sum AS float) / rating_count
    END ASC,
    created_at ASC
LIMIT 1
```

Use SQLAlchemy ORM expression — do not use raw string SQL.

## Test Specification

### `tests/db/test_postgres_buffer.py`

All unit tests mock the async session factory (no live DB):

```python
@pytest.mark.unit
async def test_should_generate_true_when_below_threshold():
    """count=10, capacity=100, threshold=0.8 → should_generate() = True."""

@pytest.mark.unit
async def test_should_generate_false_when_above_threshold():
    """count=85, capacity=100, threshold=0.8 → should_generate() = False."""

@pytest.mark.unit
async def test_insert_at_capacity_triggers_eviction():
    """When _count_active() == capacity, _evict_worst() is called before insert."""

@pytest.mark.unit
async def test_eviction_selects_lowest_rating_avg():
    """Eviction query uses rating_sum/rating_count ASC, created_at ASC order."""
    # verify via captured SQL expression or mock call args

@pytest.mark.unit
async def test_get_next_returns_oldest_active():
    """get_next() queries ORDER BY created_at ASC LIMIT 1 WHERE status='active'."""
```

Integration test (`@pytest.mark.integration`):
```python
async def test_postgres_buffer_full_cycle():
    """Insert capacity+1 Cases, verify oldest low-rated is evicted."""
```

## Definition of Done

See `dod.md` in this directory.
