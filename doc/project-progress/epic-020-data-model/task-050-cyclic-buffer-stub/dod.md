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

- [ ] `backend/src/core/cyclic_buffer.py` exists with `CyclicBuffer` (abstract) and `InMemoryCyclicBuffer` (concrete stub)
- [ ] `CyclicBuffer` is an `ABC` with four abstract async methods: `insert`, `get_next`, `evict_worst`, `size`
- [ ] `InMemoryCyclicBuffer` fully implements all four methods
- [ ] `insert` with a duplicate UUID is a no-op (does not increase size)
- [ ] `get_next` on an empty buffer returns `None`
- [ ] `get_next` cycles round-robin over all inserted IDs
- [ ] `evict_worst` removes items until buffer is at `capacity`; returns count removed
- [ ] `evict_worst` when already at or below capacity returns 0
- [ ] `InMemoryCyclicBuffer` has no database or I/O dependencies
- [ ] Docstring on `CyclicBuffer` class explicitly notes "fully implemented in E030"

## Test Criteria

- [ ] `backend/tests/core/test_cyclic_buffer.py` exists with at least 6 unit tests (see spec)
- [ ] All tests are marked `@pytest.mark.unit`
- [ ] `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [ ] `ruff check .` exits 0
- [ ] `ruff format --check .` exits 0
- [ ] `mypy src/ --strict` exits 0
- [ ] No `TODO` / `FIXME` in committed code
- [ ] `CyclicBuffer`, `InMemoryCyclicBuffer`, and all public methods have Google-style docstrings with `Args` and `Returns` sections

## Documentation Criteria

- [ ] `report.md` written with all required APM sections
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** _______________, ___________
