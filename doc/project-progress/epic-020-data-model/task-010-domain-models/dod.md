---
apm_category: dod
apm_ref: E020.T010
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E020.T010 — Domain Models + Alembic Migration

> Instructions for Coder: mark each item ✅ (met) or ❌ <note>.

---

## Functional Criteria

- [x] ✅ All nine model files exist in `backend/src/db/models/`: `bias_type.py`, `case.py`, `case_translation.py`, `ui_string.py`, `ui_string_translation.py`, `user.py`, `answer_event.py`, `rating.py`, `subscription.py`
- [x] ✅ `backend/src/db/models/__init__.py` imports all nine models
- [x] ✅ Each model uses SQLAlchemy 2.x `Mapped[T]` + `mapped_column()` style (no legacy `Column()`)
- [x] ✅ `Case.id` and all UUID PKs use `UUID(as_uuid=True)` with `default=uuid.uuid4`
- [x] ✅ `UiString.key` is `TEXT PRIMARY KEY` (not UUID)
- [x] ✅ `UiStringTranslation` has composite PK `(key, locale)` with FK to `ui_string.key ON UPDATE CASCADE ON DELETE CASCADE`
- [x] ✅ `CaseTranslation` has `UniqueConstraint("case_id", "locale")`
- [x] ✅ `Rating` has `CheckConstraint("stars BETWEEN 1 AND 5")` and `UniqueConstraint("user_id", "case_id")`
- [x] ✅ All nullable FKs (e.g. `user_id` on `AnswerEvent`, `Rating`) are correctly typed as `Mapped[UUID | None]`
- [x] ✅ `Subscription.stripe_sub_id` is nullable (E060 fills it)
- [x] ✅ No `embedding` column in `Case` (added in E030)

## Migration Criteria

- [x] ✅ `backend/alembic/versions/0002_domain_model.py` exists; obsah vychází z `alembic revision --autogenerate`, revize sjednocena na `0002` / `down_revision = "0001"` (viz report)
- [x] ✅ `alembic upgrade head` runs without error against a live PostgreSQL 16 container
- [x] ✅ `alembic check` exits 0 (no pending model changes detected after migration)
- [x] ✅ `alembic downgrade -1` runs without error (migration is reversible) — ověřeno v `tests/skeleton/test_t040.sh` (řetězec downgrade/upgrade)

## Test Criteria

- [x] ✅ `backend/tests/db/test_models.py` exists with at least one instantiation test per model (9 tests minimum)
- [x] ✅ All tests are marked `@pytest.mark.unit`
- [x] ✅ `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [x] ✅ `ruff check .` exits 0 (inside `backend/`)
- [x] ✅ `ruff format --check .` exits 0
- [x] ✅ `mypy src/ alembic/env.py --strict` exits 0
- [x] ✅ No `TODO` / `FIXME` in committed code
- [x] ✅ All public classes have Google-style docstrings (1-sentence description minimum)

## Documentation Criteria

- [x] ✅ `report.md` written with all required APM sections
- [x] ✅ Code references in report point to correct files and line numbers

---

**Filled by Coder:** Composer, 2026-05-10
