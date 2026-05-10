---
apm_category: task-spec
apm_ref: E020.T010
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T010 — Domain Models + Alembic Migration

## Goal

Define all nine SQLAlchemy 2.x ORM models for the MVP domain and produce a
reviewed, working Alembic migration `0002_domain_model` that upgrades a clean
database from the empty baseline.

## Depends on

None (first task in E020; starts in parallel with T050).

## Inputs

- `backend/src/db/base.py` — `DeclarativeBase` (exists from E010)
- `backend/src/db/models/__init__.py` — currently empty; must import all models after this task
- `backend/alembic/versions/0001_initial.py` — empty baseline migration
- `backend/alembic/env.py` — async Alembic env (exists from E010)
- `doc/project-progress/spec.md` — entity list, i18n strategy
- `doc/project-progress/epic-020-data-model/plan.md` — exact field specs (§ T010)

## Outputs

New files in `backend/src/db/models/`:

| File | Entity | Table name |
|------|--------|-----------|
| `bias_type.py` | `BiasType` | `bias_type` |
| `case.py` | `Case` | `case` (quoted) |
| `case_translation.py` | `CaseTranslation` | `case_translation` |
| `ui_string.py` | `UiString` | `ui_string` |
| `ui_string_translation.py` | `UiStringTranslation` | `ui_string_translation` |
| `user.py` | `User` | `user` (quoted) |
| `answer_event.py` | `AnswerEvent` | `answer_event` |
| `rating.py` | `Rating` | `rating` |
| `subscription.py` | `Subscription` | `subscription` |

Updated file:
- `backend/src/db/models/__init__.py` — imports all nine models

New migration:
- `backend/alembic/versions/0002_domain_model.py`

New tests:
- `backend/tests/db/test_models.py`

## Implementation Notes

### SQLAlchemy style
Use `Mapped[T]` + `mapped_column()` (SQLAlchemy 2.x declarative style). See `plan.md § T010`
for exact fields, types, defaults, constraints, and FK options for every model.

### Reserved table names
`"case"` and `"user"` are PostgreSQL reserved words — use `__tablename__ = '"case"'`? No.
Use `__tablename__ = "case"` but wrap with `quoted_name("case", True)` OR simply keep
`__tablename__ = "case"` — SQLAlchemy quotes it automatically when the identifier matches
a reserved word. Verify this works with Alembic autogenerate.

### source_hash computation
`sha256(f"{key}|{title}|{description}".encode("utf-8")).hexdigest()`

For `CaseTranslation`, `source_hash` is `sha256` of the concatenated English `title + question + options_json + explanation` — exact formula to be consistent with E030 generator.
Use: `sha256((en_title + "|" + en_question + "|" + json.dumps(en_options, sort_keys=True) + "|" + en_explanation).encode()).hexdigest()`

### Alembic workflow
Run inside the `backend` Docker service (or local virtualenv with DB accessible):

```bash
# Inside backend container:
alembic revision --autogenerate -m "domain_model"
# Review generated file — ensure all 9 tables and constraints appear
alembic upgrade head
alembic check   # must exit 0 (no pending changes)
```

### No pgvector in E020
The `embedding` column (Vector type) on `Case` is added in E030 when the vector extension
and provider are decided (ADR-004). Do NOT add it here.

### `models/__init__.py`
Must import all models so Alembic `env.py` picks up their metadata:

```python
from src.db.models.bias_type import BiasType
from src.db.models.case import Case
# … all nine models
__all__ = ["BiasType", "Case", …]
```

## Test Specification

File: `backend/tests/db/test_models.py`, marker `unit`

For each model, write at least one test:

```python
@pytest.mark.unit
def test_bias_type_instantiation() -> None:
    bt = BiasType(slug="anchoring", name_en="Anchoring Bias", description_en="…", source_hash="abc")
    assert bt.slug == "anchoring"

@pytest.mark.unit
def test_ui_string_instantiation() -> None:
    us = UiString(key="app_title", title="Cognitive Bias Tester",
                  description="App name", source_hash="abc123")
    assert us.key == "app_title"

# … etc.
```

No DB connection required — these are pure ORM object tests.

## Regression Check

After completing this task, run inside the `backend` container:

```bash
ruff check .
ruff format --check .
mypy src/ --strict
pytest -m "not integration" -q
```

All must exit 0. Do not proceed if any fail.

## APM Output (required at task end)

After all code is implemented and tests pass, Coder MUST:

1. Write `report.md` in this directory (`task-010-domain-models/report.md`) — all APM sections in Czech.
2. Fill all checkboxes in `dod.md` in this directory with ✅ or ❌ + note.

These files are in `doc/` but are the Coder's responsibility to create/fill. The "do not modify doc/**" constraint in plan.md refers to spec files, plan files, roadmap, and ADRs — NOT to this task's own `report.md` and `dod.md`.

## Definition of Done

See [dod.md](dod.md).
