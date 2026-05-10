---
apm_category: dod
apm_ref: E020.T030
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T030 — Seed Data

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ `backend/src/db/seed/bias_types.json` contains exactly 5 bias type objects (slugs: `anchoring`, `framing`, `loss_aversion`, `confirmation_bias`, `sunk_cost`)
- [x] ✅ `backend/src/db/seed/cases.json` contains exactly 25 Case objects (5 per bias type)
- [x] ✅ Each Case has exactly 4 options (`A`, `B`, `C`, `D`) and a valid `correct_option` (0–3)
- [x] ✅ Each Case uses at least one parametric placeholder (e.g. `{local_first_name}`, `{currency_amount_small}`) in `question` or `options`
- [x] ✅ Cases span at least 3 different real-world domains (finance, health, work, consumer, social, etc.)
- [x] ✅ `backend/src/db/seed/ui_strings.json` contains all keys from `frontend/src/locales/en.json` plus any additional MVP UI chrome keys; each entry has `title` and `description`
- [x] ✅ `backend/src/db/seed/seed.py` is runnable as `python -m src.db.seed.seed`
- [x] ✅ `seed.py` is idempotent — running it twice does not produce duplicate rows or unhandled errors (presence checks before add)
- [x] ✅ `seed.py` logs inserted vs skipped counts per entity type at INFO level
- [x] ✅ `source_hash` is computed at runtime (not hardcoded in JSON)

## Test Criteria

- [x] ✅ `backend/tests/db/test_seed.py` exists with at least 4 unit tests covering: first-run inserts, idempotent skip, 25 cases count, source_hash computation
- [x] ✅ All tests are marked `@pytest.mark.unit`
- [x] ✅ `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [x] ✅ `ruff check .` exits 0
- [x] ✅ `ruff format --check .` exits 0
- [x] ✅ `mypy src/ --strict` exits 0
- [x] ✅ No `TODO` / `FIXME` in committed code
- [x] ✅ JSON files are UTF-8, 2-space indented, valid JSON (parseable by `json.loads`)

## Content Quality Criteria

- [x] ✅ All 25 Cases are realistic and self-contained (no external knowledge required)
- [x] ✅ The `explanation` field for each Case clearly explains why the `correct_option` is correct and names the bias
- [x] ✅ No Case is a near-duplicate of another (different scenario, different framing)

## Documentation Criteria

- [x] ✅ `report.md` written with all required APM sections
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-10
