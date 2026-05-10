---
apm_category: task-report
apm_ref: E020.T060
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Report: E020.T060 — Corrections & DoD Integrity Fix

## Co bylo implementováno

Retrospektivní APM reporty pro T010, T020 a T030; úprava `cases.json` tak, aby index správné odpovědi 0–3 byl vyvážený (~6–7 na index, minimum 4), při zachování textů odpovědí pouze přeuspořádáním pole `options` a aktualizací `label` A–D. CI krok Mypy rozšířen o `alembic/env.py` (v repozitáři již bylo v `ci.yml` ověřeno). DoD u T020/T030 sladěno s příkazem `mypy src/ alembic/env.py --strict`.

## Vstupy a výstupy

- **Přečteno:** `task-060-corrections/spec.md`, `plan.md`, task spec T010–T030, `execute-task` skill
- **Vytvořeno:** `task-010-domain-models/report.md`, `task-020-repository-layer/report.md`, `task-030-seed-data/report.md`, tento `task-060-corrections/report.md`
- **Změněno:** `backend/src/db/seed/cases.json`, `task-020-repository-layer/dod.md`, `task-030-seed-data/dod.md`, `task-060-corrections/dod.md`, `.github/workflows/ci.yml` (pokud nebyl mypy řádek již dříve aktualizován — stav v době merge)

## Použité metody a rozhodnutí

- Pro přeskupení odpovědí: správná varianta byla vždy na indexu 1; pro i-tý záznam (0–24) cíl `t = i % 4`, nové pořadí `[wrong[:t] + [correct] + wrong[t:]]` kde `wrong` jsou položky na původních indexech 0, 2, 3. Výsledná distribuce `{0: 7, 1: 6, 2: 6, 3: 6}`.

## Odchylky od spec.md

—

## Reference do kódu

- `backend/src/db/seed/cases.json` — rozložení `correct_option` a přeskupené `options`
- `.github/workflows/ci.yml` — job Backend quality, krok Mypy
- `doc/project-progress/epic-020-data-model/task-010-domain-models/report.md` — zápis Integer vs SmallInteger v § Odchylky

## Výsledek regresního testu

✅ V Docker image backendu: `ruff check .`, `ruff format --check .`, `mypy src/ alembic/env.py --strict`, `pytest -m "not integration" -q` — úspěšně. Integrační job (Alembic + seed + `GET /v1/i18n/en`) ověří GitHub Actions proti čisté PostgreSQL službě; lokální svazek může mít zastaralý `alembic_version`.

## Definition of Done

Viz [dod.md](dod.md).
