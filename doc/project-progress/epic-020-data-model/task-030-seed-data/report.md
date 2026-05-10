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

JSON fixtury (`bias_types.json`, `cases.json`, `ui_strings.json`) a skript `python -m src.db.seed.seed` načítající data přes repozitáře s idempotentními kontrolami (přítomnost záznamu → přeskočení). `compute_source_hash` / `compute_case_translation_hash` počítají SHA-256 za běhu. Logování statistik insert vs skip na úrovni INFO.

## Vstupy a výstupy

- **Přečteno:** `task-030-seed-data/spec.md`, `frontend/src/locales/en.json` (klíče UI)
- **Vytvořeno:** `backend/src/db/seed/*.json`, `backend/src/db/seed/seed.py`, `backend/tests/db/test_seed.py`
- **Změněno:** případné propojení v `src.main` nebo CLI dle integračního nastavení projektu

## Použité metody a rozhodnutí

- Idempotence přes dotazy do repozitářů před `add`, žádné duplicity při opakovaném běhu.
- Cases: 25 scénářů (5× slug biasu), každý s 4 možnostmi a vysvětlením.
- Distribuce `correct_option` byla později upřesněna v E020.T060 (rovnoměrnější rozložení indexů 0–3).

## Odchylky od spec.md

—

## Reference do kódu

- `backend/src/db/seed/seed.py:44-84` — hash funkce a kanonický obsah case záznamu
- `backend/src/db/seed/seed.py` — `run_seed_with_repos`, `load_fixtures`
- `backend/src/db/seed/cases.json` — 25 case záznamů (po T060 s rozložením `correct_option`)
- `backend/tests/db/test_seed.py` — první běh, skip biasů, 25 cases, `source_hash`

## Výsledek regresního testu

✅ `pytest -m "not integration" -q`; integrační smoke API po seedu v CI (`GET /v1/i18n/en`).

## Definition of Done

Viz [dod.md](dod.md).
