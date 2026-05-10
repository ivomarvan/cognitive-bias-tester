---
apm_category: task-report
apm_ref: E020.T020
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T020 — Repository Layer

## Co bylo implementováno

Generická báze `Repository[ModelT]` s `add`/`delete` používajícími `flush()` (transakce na volajícím). Deset souborů repozitářů pro entity včetně `UiStringRepository` s `LEFT OUTER JOIN` pro překlady a `INSERT ... ON CONFLICT` pro upsert překladu. `CaseRepository.update_rating()` atomicky přes jeden `UPDATE`.

## Vstupy a výstupy

- **Přečteno:** `task-020-repository-layer/spec.md`, existující modely a `AsyncSession`
- **Vytvořeno:** `backend/src/db/repositories/*.py` (10 modulů včetně `base.py`)
- **Změněno:** `backend/src/db/repositories/__init__.py`, `backend/tests/db/test_repositories.py`

## Použité metody a rozhodnutí

- Repozitáře přijímají `AsyncSession` v konstruktoru (bez globální session).
- Unit testy používají `AsyncMock(spec=AsyncSession)` — bez živé databáze.
- DRY: společná logika v `Repository` base třídě.

## Odchylky od spec.md

—

## Reference do kódu

- `backend/src/db/repositories/base.py` — abstraktní `Repository[ModelT]`
- `backend/src/db/repositories/ui_string.py` — join a PostgreSQL upsert překladů
- `backend/src/db/repositories/case.py` — `update_rating` jedním SQL příkazem
- `backend/tests/db/test_repositories.py` — pokrytí happy path a edge cases pro veřejné metody

## Výsledek regresního testu

✅ `pytest -m "not integration" -q` — všechny unit testy zelené (ověřeno při dokončení E020.T020 a regresi v E020.T060).

## Definition of Done

Viz [dod.md](dod.md).
