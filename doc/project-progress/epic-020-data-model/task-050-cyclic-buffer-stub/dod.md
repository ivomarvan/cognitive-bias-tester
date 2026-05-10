---
apm_category: dod
apm_ref: E020.T050
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T050 — Cyclic Buffer Stub

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `backend/src/core/cyclic_buffer.py` exists with `CyclicBuffer` (abstract) and `InMemoryCyclicBuffer` (concrete stub)
- [x] ✅ `CyclicBuffer` is an `ABC` with four abstract async methods: `insert`, `get_next`, `evict_worst`, `size`
- [x] ✅ `InMemoryCyclicBuffer` fully implements all four methods
- [x] ✅ `insert` with a duplicate UUID is a no-op (does not increase size)
- [x] ✅ `get_next` on an empty buffer returns `None`
- [x] ✅ `get_next` cycles round-robin over all inserted IDs
- [x] ✅ `evict_worst` removes items until buffer is at `capacity`; returns count removed
- [x] ✅ `evict_worst` when already at or below capacity returns 0
- [x] ✅ `InMemoryCyclicBuffer` has no database or I/O dependencies
- [x] ✅ Docstring on `CyclicBuffer` class explicitly notes "fully implemented in E030"

## Test Criteria

- [x] ✅ `backend/tests/core/test_cyclic_buffer.py` exists with at least 6 unit tests (see spec)
- [x] ✅ All tests are marked `@pytest.mark.unit`
- [x] ✅ `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [x] ✅ `ruff check .` exits 0
- [x] ✅ `ruff format --check .` exits 0
- [x] ✅ `mypy src/ --strict` exits 0
- [x] ✅ No `TODO` / `FIXME` in committed code
- [x] ✅ `CyclicBuffer`, `InMemoryCyclicBuffer`, and all public methods have Google-style docstrings with `Args` and `Returns` sections

## Documentation Criteria

- [x] ✅ `report.md` written with all required APM sections
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-10
