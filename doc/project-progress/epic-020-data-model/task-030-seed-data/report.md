---
apm_category: task-report
apm_ref: E020.T030
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T030 — Seed Data

## Co bylo implementováno

JSON fixtury: přesně 5 typů zkreslení (`bias_types.json`), 25 gold-standard scénářů (`cases.json`, 5× variant 0–4 na slug, parametrické placeholdery v každém případu), rozšířené UI řetězce včetně mapování z `frontend/src/locales/en.json` (`app`→`app_title`, `home`→`home_heading`) a dalšího MVP chrome (`ui_strings.json`). `seed.py` načítá fixtury z adresáře modulu, v jedné transakci (`async_session` + `session.begin()`) volá `run_seed_with_repos` s T020 repozitáři: bias podle `get_by_slug`, case podle `(bias_type_id, variant)` mezi aktivními řádky, `UiString` podle textového PK. `source_hash` pro `UiString` = SHA-256 z `key|title|description`, pro `CaseTranslation` z kanonického JSON obsahu. Logování INFO se součty inserted/skipped.

## Vstupy a výstupy

- **Přečteno:** `task-030-seed-data/spec.md`, `plan.md` § T030, `frontend/src/locales/en.json`.
- **Vytvořeno:** `backend/src/db/seed/__init__.py`, `bias_types.json`, `cases.json`, `ui_strings.json`, `seed.py`, `backend/tests/db/test_seed.py`, `report.md`.
- **Změněno:** `doc/.../task-030-seed-data/dod.md`.

## Použité metody a rozhodnutí

- **Idempotence:** primárně existence před `add` (ne `IntegrityError` per řádek), aby zůstala jedna transakce bez savepointů.
- **CaseTranslation:** hash z `title`, `question`, `options`, `correct_option`, `explanation`, `locale` — stabilní při opakovaném seedu stejného obsahu.

## Reference do kódu

- `backend/src/db/seed/seed.py` — `run_seed_with_repos`, `compute_source_hash`, `seed()`
- `backend/src/db/seed/cases.json` — 25 scénářů
- `backend/tests/db/test_seed.py` — mockované repozitáře

## Výsledek regresního testu

✅ `ruff check`, `ruff format --check`, `mypy src/ --strict`, `pytest -m "not integration"` — OK.

## Definition of Done

Viz [dod.md](dod.md) — všechna kritéria ✅.
