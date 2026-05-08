---
apm_category: task-report
apm_ref: E010.T010
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

<!-- Aktualizováno: poznámka o opakované kontrole DoD — viz sekce níže. -->

# Task Report: E010.T010 — Project structure, `.gitignore`, root `README.md` skeleton, ADR-001 + ADR-002

---

## Co bylo implementováno

- Zřízena kostra webové aplikace podle `06-project-structure.mdc`: `backend/`, `frontend/`, `doc/` (včetně `architecture/decisions/`, `guides/`, `external/`), `experiments/`, `nogit_data/` a `tests/skeleton/`.
- Přidán kořenový `.gitignore` (sekrety, IDE, OS, logy, Python, Node, Docker, generovaná dokumentace), přepsán kořenový `README.md` na čitelný placeholder s odkazy na spec a roadmapu.
- Doplněny ADR-001 (PostgreSQL) a ADR-002 (etický rámec + proces amendmántů).
- Přidán spustitelný skript `tests/skeleton/test_t010.sh` ověřující existenci artefaktů, klíčové řádky v `.gitignore` a strukturu ADR.

---

## Vstupy a výstupy

### Přečteno

- `doc/project-progress/epic-010-skeleton/task-010-project-structure/spec.md`
- `dod.md`
- `.cursor/README.project_management.md`
- `doc/project-progress/spec.md` (tabulka *Key Technical Decisions*)
- `.cursor/rules/02-git.mdc`
- `.cursor/rules/06-project-structure.mdc`
- `.cursor/rules/10-python.mdc` (sekce `.gitignore` — pravidlo `11-vuejs-vite-tailwind.mdc` v repozitáři nebylo nalezeno; Node vzory doplněny konvencí Vite/npm)

### Vytvořeno

- `backend/.gitkeep`
- `frontend/.gitkeep`
- `doc/guides/.gitkeep`
- `doc/external/.gitkeep`
- `nogit_data/.gitkeep`
- `experiments/.gitkeep`
- `doc/architecture/decisions/ADR-001-use-postgresql.md`
- `doc/architecture/decisions/ADR-002-ethics-framework.md`
- `tests/skeleton/test_t010.sh`

### Změněno

- `.gitignore` (nový obsah)
- `README.md` (náhrada placeholderu)

### Nedotčeno (Context Bundle)

- `.cursor/**`
- `LICENSE`
- `doc/project-progress/brief.md`
- `doc/project-progress/spec.md`
- `doc/project-progress/roadmap.md`
- `doc/project-progress/GLOSSARY.md`

---

## Použité metody a rozhodnutí

### `.gitignore` vs. `nogit_data/.gitkeep`

Dodržen požadavek na doslovný řádek `nogit_data/` (test T010 + konvence z `02-git.mdc`). Git pak ignoruje cestu jako celek; sledovatelný marker `.gitkeep` vyžaduje při prvním zařazení `git add -f nogit_data/.gitkeep`. Alternativa `nogit_data/*` + negace by odporovala testu vyžadujícímu řádek `nogit_data/`.

### ADR

Text v angličtině; ADR-001 explicitně cituje řádek **3** (*Database*) z `doc/project-progress/spec.md`, ADR-002 řádek **15** (*Ethics framework*) a obsahuje zakázané/obecně přijatelné segmenty a proces změny přes nový ADR (bez tiché editace).

### Test

POSIX bash, `set -euo pipefail`, ověření README klíčových slov nad rámec minimálního zadání kvůli formulaci „missing keyword“ ve specifikaci testu.

---

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `.gitignore` | 1-63 | Kořenová pravidla ignorování (včetně požadovaných doslovných řádků pro T010). |
| `README.md` | 1-37 | Titulek, popis, stav MVP, Quick start, struktura, odkazy na `spec.md` / `roadmap.md`, poznámka k licenci MIT. |
| `doc/architecture/decisions/ADR-001-use-postgresql.md` | 1-25 | ADR-001 včetně *Considered alternatives* a zamítnutí SQLite. |
| `doc/architecture/decisions/ADR-002-ethics-framework.md` | 1-44 | ADR-002 včetně misijního zarovnání, seznamů *We will not sell to* / *We are open to* a *Amendment process*. |
| `tests/skeleton/test_t010.sh` | 1-80 | Kontrolní skript (happy path, `.gitignore`, struktura ADR, klíčová slova README). |
| `nogit_data/.gitkeep` | 1 | Jedna řádka komentáře; jediný sledovaný soubor pod `nogit_data/`. |

---

## Výsledek regresního testu

| Command / scope | Result | Notes |
|-----------------|--------|-------|
| `bash tests/skeleton/test_t010.sh` | ✅ exit **0** (`test_t010: OK`) | — |
| `pytest tests/ -v --tb=short` | ✅ exit **5**, **0** testů nashromážděno | Standardní pytest při absenci `test_*.py`; žádná chyba sběrače ani selhání assertů. |

---

## Definition of Done

Všechna kritéria v [dod.md](dod.md) jsou vyplněna a označena jako splněná (✅), včetně poznámek k `nogit_data/.gitkeep` a k pytest exit kódu **5** při nulovém počtu testů.

---

## Poznámky — opakovaná kontrola DoD

Dne **2026-05-08** byl [dod.md](dod.md) znovu použit jako kontrolní seznam: proběhla systematická verifikace funkcionality (strom souborů dle `spec.md`), testů (`bash tests/skeleton/test_t010.sh` → exit **0**), spustitelnosti a hlavičky skriptu, běhu `pytest tests/` (**0** testů, exit **5**), absence `TODO`/`FIXME` v artefaktech T010 (README, ADR, `test_t010.sh`) a konzistence dokumentace.

Výsledek je zapsán v dod v sekci **„Záznam opakované kontroly DoD“**; závěr zůstává **vše ✅** bez nově nalezených rozporů se zadáním. Opraveny byly jen čísla řádků v sekci „Reference do kódu“ podle aktuálního `wc -l`.
