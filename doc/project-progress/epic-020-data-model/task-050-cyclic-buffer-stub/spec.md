---
apm_category: task-spec
apm_ref: E020.T050
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T050 — Cyclic Buffer Stub

## Goal

Define the typed `CyclicBuffer` abstract interface and an in-memory stub implementation
(`InMemoryCyclicBuffer`) that allows unit tests to run without a database. The full
production implementation (DB-backed, with eviction by composite rating/age score) is
deferred to E030.

## Depends on

None (can run in parallel with T010).

## Inputs

- `backend/src/core/config.py` and `backend/src/core/logging.py` — style reference
- `doc/project-progress/spec.md` — LLM cache cyclic buffer description
- `doc/project-progress/epic-020-data-model/plan.md` — interface spec (§ T050)

## Outputs

- `backend/src/core/cyclic_buffer.py`
- `backend/tests/core/test_cyclic_buffer.py`

## Implementation Notes

### Abstract interface

```python
# backend/src/core/cyclic_buffer.py
from abc import ABC, abstractmethod
from uuid import UUID


class CyclicBuffer(ABC):
    """Interface for the Case cyclic buffer — fully implemented in E030.

    The buffer holds a capped ordered set of active Case IDs. Cases are:
    - inserted after LLM generation and judge validation (E030)
    - retrieved round-robin by locale / bias type for Mode 1 serving
    - evicted by composite (rating_avg, age) score when the buffer exceeds capacity
    """

    @abstractmethod
    async def insert(self, case_id: UUID) -> None:
        """Add a Case ID to the buffer. No-op if already present.

        Args:
            case_id: UUID of the Case to add.
        """

    @abstractmethod
    async def get_next(
        self,
        locale: str,
        bias_type_slug: str | None = None,
    ) -> UUID | None:
        """Return the next Case ID for the given locale, or None if the buffer is empty.

        Args:
            locale: IETF language tag of the requesting user.
            bias_type_slug: Optional filter — if given, only Cases of this
                bias type are eligible. None means any bias type.

        Returns:
            A Case UUID, or None when no eligible Cases are available.
        """

    @abstractmethod
    async def evict_worst(self) -> int:
        """Evict Cases until buffer is at or below capacity.

        Eviction criterion (implemented in E030): lowest composite score
        of (rating_avg, recency). Stub may evict arbitrarily.

        Returns:
            Number of Case IDs removed.
        """

    @abstractmethod
    async def size(self) -> int:
        """Return the current number of Case IDs in the buffer.

        Returns:
            Non-negative integer count.
        """


class InMemoryCyclicBuffer(CyclicBuffer):
    """Deterministic in-memory stub for unit tests — NOT for production use.

    Stores UUIDs in insertion order (list). ``get_next`` cycles round-robin
    over all stored IDs, ignoring locale and bias_type_slug filters.
    ``evict_worst`` removes items from the END of the insertion-order list.
    """

    def __init__(self, capacity: int = 100) -> None:
        self._capacity = capacity
        self._items: list[UUID] = []
        self._cursor: int = 0

    async def insert(self, case_id: UUID) -> None:
        if case_id not in self._items:
            self._items.append(case_id)

    async def get_next(
        self,
        locale: str,
        bias_type_slug: str | None = None,
    ) -> UUID | None:
        if not self._items:
            return None
        item = self._items[self._cursor % len(self._items)]
        self._cursor += 1
        return item

    async def evict_worst(self) -> int:
        excess = max(0, len(self._items) - self._capacity)
        self._items = self._items[:len(self._items) - excess]
        return excess

    async def size(self) -> int:
        return len(self._items)
```

### Note on production implementation
The stub deliberately ignores `locale` and `bias_type_slug` in `get_next`. The production
`DbCyclicBuffer` in E030 will join with `case_translation` and `bias_type` tables to filter
correctly. This is acceptable — the stub's purpose is to satisfy the interface contract for
unit tests, not to implement business logic.

## Test Specification

File: `backend/tests/core/test_cyclic_buffer.py`, marker `unit`

```python
import pytest
from uuid import uuid4
from src.core.cyclic_buffer import InMemoryCyclicBuffer


@pytest.mark.unit
async def test_insert_increases_size() -> None:
    buf = InMemoryCyclicBuffer(capacity=10)
    await buf.insert(uuid4())
    assert await buf.size() == 1

@pytest.mark.unit
async def test_insert_duplicate_is_noop() -> None:
    buf = InMemoryCyclicBuffer(capacity=10)
    uid = uuid4()
    await buf.insert(uid)
    await buf.insert(uid)
    assert await buf.size() == 1

@pytest.mark.unit
async def test_get_next_empty_returns_none() -> None:
    buf = InMemoryCyclicBuffer(capacity=10)
    assert await buf.get_next(locale="en") is None

@pytest.mark.unit
async def test_get_next_cycles_round_robin() -> None:
    buf = InMemoryCyclicBuffer(capacity=10)
    ids = [uuid4() for _ in range(3)]
    for uid in ids:
        await buf.insert(uid)
    results = [await buf.get_next(locale="en") for _ in range(6)]
    assert results == ids + ids  # full round-robin cycle twice

@pytest.mark.unit
async def test_evict_worst_removes_excess() -> None:
    buf = InMemoryCyclicBuffer(capacity=2)
    for _ in range(3):
        await buf.insert(uuid4())
    evicted = await buf.evict_worst()
    assert evicted == 1
    assert await buf.size() == 2

@pytest.mark.unit
async def test_evict_worst_within_capacity_is_noop() -> None:
    buf = InMemoryCyclicBuffer(capacity=5)
    await buf.insert(uuid4())
    evicted = await buf.evict_worst()
    assert evicted == 0
    assert await buf.size() == 1
```

## Regression Check

```bash
ruff check .
ruff format --check .
mypy src/ --strict
pytest -m "not integration" -q
```

All must exit 0.

## Definition of Done

See [dod.md](dod.md).
