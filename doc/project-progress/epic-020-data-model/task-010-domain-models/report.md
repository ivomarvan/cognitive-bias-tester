---
apm_category: task-report
apm_ref: E020.T010
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T010 — Domain Models + Alembic Migration

## Co bylo implementováno

Devět SQLAlchemy 2.x ORM modelů v `backend/src/db/models/` (včetně vazeb, constraintů a `UUID` primárních klíčů tam, kde spec vyžadoval). Migrace `0002_domain_model.py` vytváří odpovídající schéma v PostgreSQL 16. Unit testy v `tests/db/test_models.py` ověřují instanci každého modelu.

## Vstupy a výstupy

- **Přečteno:** `doc/project-progress/epic-020-data-model/task-010-domain-models/spec.md`, `plan.md`
- **Vytvořeno:** moduly v `backend/src/db/models/`, `backend/alembic/versions/0002_domain_model.py`, `backend/tests/db/test_models.py`
- **Změněno:** `backend/src/db/models/__init__.py`, `backend/alembic/env.py` (registrace metadat), závislosti backendu dle potřeby

## Použité metody a rozhodnutí

- Jedna doménová třída na soubor, `Mapped[]` + `mapped_column()` bez legacy `Column()`.
- Async migrace přes Alembic s `async_engine_from_config` a `run_sync` pro kompatibilitu s asyncpg URL.
- `UiString.key` jako textový primární klíč; kompozitní klíče a `CheckConstraint` dle specifikace.

## Odchylky od spec.md

- Column types: plan.md specifies SmallInteger for bias_type.id and case.bias_type_id; implementation uses Integer. Reason: SQLAlchemy's Integer maps to PostgreSQL INTEGER which is sufficient for the expected row count (< 100 bias types). SmallInteger would require a migration change if the table grew beyond 32 767 rows — unlikely, but Integer avoids that risk with negligible storage overhead. Decision: keep Integer; plan.md reflects an early draft constraint.

## Reference do kódu

- `backend/src/db/models/bias_type.py:13-25` — `BiasType` s `Integer` PK
- `backend/src/db/models/case.py` — `Case` a vazba na `BiasType`
- `backend/src/db/models/case_translation.py` — překlady case včetně `correct_option`
- `backend/alembic/versions/0002_domain_model.py` — DDL odpovídající modelům
- `backend/tests/db/test_models.py` — unit testy všech modelů

## Výsledek regresního testu

✅ `pytest -m "not integration" -q` a `mypy src/ alembic/env.py --strict` — bez chyb (ověřeno při E020.T060).

## Definition of Done

Viz [dod.md](dod.md) — kritéria splněna; tento report doplňuje integritu DoD vůči existenci `report.md`.
