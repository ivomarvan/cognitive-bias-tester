---
apm_category: task-dod
apm_ref: E030.T050
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T050 — DB-backed Cyclic Buffer

## Implementation

- [ ] `backend/src/db/buffer/postgres_buffer.py` — `PostgresCyclicBuffer` class exists
- [ ] `PostgresCyclicBuffer` implements all methods of the `CyclicBuffer` protocol
  (`get_next`, `insert`, `should_generate`)
- [ ] `_evict_worst()` uses composite ORDER BY `(rating_avg ASC, created_at ASC)`
  expressed as SQLAlchemy ORM expression (no raw SQL strings)
- [ ] `insert()` calls `_evict_worst()` when `_count_active() >= capacity`

## Settings

- [ ] `BUFFER_CAPACITY` and `BUFFER_REFILL_THRESHOLD` added to `Settings`

## Tests

- [ ] `tests/db/test_postgres_buffer.py` — all 5 unit tests pass
- [ ] `should_generate` returns True when below threshold
- [ ] `should_generate` returns False when above threshold
- [ ] eviction is triggered on insert when at capacity
- [ ] eviction ORDER BY verified (rating_avg ASC, created_at ASC)
- [ ] `get_next` ORDER BY created_at ASC verified
- [ ] Integration test `test_postgres_buffer_full_cycle` marked as `@pytest.mark.integration`
- [ ] `pytest -m "not integration" -q` — full unit suite green, no regressions

## Quality

- [ ] `mypy src/ alembic/env.py --strict` — clean
- [ ] `ruff check . && ruff format --check .` — clean
- [ ] `InMemoryCyclicBuffer` from E020/T050 is NOT removed (still used in unit tests elsewhere)

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes reflect actual state (DoD integrity rule)
