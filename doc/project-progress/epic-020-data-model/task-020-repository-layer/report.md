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

Přidán adresář `backend/src/db/repositories/` s generickou bází `Repository[ModelT]` (CRUD přes `get_by_id`, `list`, `add`, `delete` s `flush`, bez `commit`) a devíti konkrétními repozitáři dle `plan.md` § T020. `UiStringRepository` obsahuje `get_all_with_translation` s `outerjoin`, `upsert_translation` přes `sqlalchemy.dialects.postgresql.insert` a `on_conflict_do_update`. `CaseRepository.update_rating` používá jeden `update()` s atomickým přičtením k `rating_sum` / `rating_count` a `updated_at=func.now()`. Unit testy mockují `AsyncSession` v `backend/tests/db/test_repositories.py`.

## Vstupy a výstupy

- **Přečteno:** `task-020-repository-layer/spec.md`, `dod.md`, `epic-020-data-model/plan.md` § T020, modely T010, `session.py`.
- **Vytvořeno:** `backend/src/db/repositories/*.py` (10 souborů), `backend/tests/db/test_repositories.py`, tento `report.md`.
- **Změněno:** `doc/.../task-020-repository-layer/dod.md` (zaškrtnutí).

## Použité metody a rozhodnutí

- **`model_cls`:** každá podtřída definuje `ClassVar[type[...]]` kvůli `session.get()` / `select()`; u generické báze `get_by_id` / `list` používají `cast` kvůli striktnímu mypy u `DeclarativeBase` vs konkrétní model.
- **`get_all_with_translation`:** návratová hodnota sestavena jako `[(row[0], row[1]) for row in result.all()]` kvůli typům joinu (outer join → `None` u překladu).
- **API vrstva:** endpointy ani `Depends` factory v `spec` nejsou — pouze datová vrstva.

## Reference do kódu

- `backend/src/db/repositories/base.py` — generický Repository
- `backend/src/db/repositories/ui_string.py` — outer join + PostgreSQL upsert
- `backend/src/db/repositories/case.py` — `update_rating`
- `backend/tests/db/test_repositories.py` — mocked AsyncSession testy

## Výsledek regresního testu

✅ `ruff check`, `ruff format --check`, `mypy src/ --strict`, `pytest -m "not integration"` — v kontejneru backend OK.

## Definition of Done

Viz [dod.md](dod.md) — všechna kritéria ✅.
