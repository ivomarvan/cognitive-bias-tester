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

- [ ] All nine model files exist in `backend/src/db/models/`: `bias_type.py`, `case.py`, `case_translation.py`, `ui_string.py`, `ui_string_translation.py`, `user.py`, `answer_event.py`, `rating.py`, `subscription.py`
- [ ] `backend/src/db/models/__init__.py` imports all nine models
- [ ] Each model uses SQLAlchemy 2.x `Mapped[T]` + `mapped_column()` style (no legacy `Column()`)
- [ ] `Case.id` and all UUID PKs use `UUID(as_uuid=True)` with `default=uuid.uuid4`
- [ ] `UiString.key` is `TEXT PRIMARY KEY` (not UUID)
- [ ] `UiStringTranslation` has composite PK `(key, locale)` with FK to `ui_string.key ON UPDATE CASCADE ON DELETE CASCADE`
- [ ] `CaseTranslation` has `UniqueConstraint("case_id", "locale")`
- [ ] `Rating` has `CheckConstraint("stars BETWEEN 1 AND 5")` and `UniqueConstraint("user_id", "case_id")`
- [ ] All nullable FKs (e.g. `user_id` on `AnswerEvent`, `Rating`) are correctly typed as `Mapped[UUID | None]`
- [ ] `Subscription.stripe_sub_id` is nullable (E060 fills it)
- [ ] No `embedding` column in `Case` (added in E030)

## Migration Criteria

- [ ] `backend/alembic/versions/0002_domain_model.py` exists and was generated via `--autogenerate`
- [ ] `alembic upgrade head` runs without error against a live PostgreSQL 16 container
- [ ] `alembic check` exits 0 (no pending model changes detected after migration)
- [ ] `alembic downgrade -1` runs without error (migration is reversible)

## Test Criteria

- [ ] `backend/tests/db/test_models.py` exists with at least one instantiation test per model (9 tests minimum)
- [ ] All tests are marked `@pytest.mark.unit`
- [ ] `pytest -m "not integration" -q` exits 0

## Code Quality Criteria

- [ ] `ruff check .` exits 0 (inside `backend/`)
- [ ] `ruff format --check .` exits 0
- [ ] `mypy src/ --strict` exits 0
- [ ] No `TODO` / `FIXME` in committed code
- [ ] All public classes have Google-style docstrings (1-sentence description minimum)

## Documentation Criteria

- [ ] `report.md` written with all required APM sections
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** _______________, ___________
