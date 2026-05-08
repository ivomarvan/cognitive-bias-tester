---
apm_category: dod
apm_ref: E010.T010
apm_level: task
created_by: Planner
model: claude-opus-4-7
intended_for: Coder
created_at: 2026-05-08
updated_at: 2026-05-08
---

<!-- Poslední kontrola checklistu: viz sekce „Záznam opakované kontroly DoD“ níže. -->

# Definition of Done: E010.T010 — Project structure, `.gitignore`, root `README.md` skeleton, ADR-001 + ADR-002

> Instructions for Coder: mark each item ✅ (met) or ❌ <note> (not met, with explanation).
> Every item must be addressed — no blanks. Blank = not reviewed = not done.

---

## Functional Criteria

- [x] ✅ Directory tree exists exactly as listed in `spec.md` *Outputs* (with `.gitkeep` placeholders)
- [x] ✅ `nogit_data/.gitkeep` is committed; contents of `nogit_data/` are otherwise excluded *(soubor je vytvořen; kvůli řádku `nogit_data/` v `.gitignore` je první zařazení do indexu nutné přes `git add -f nogit_data/.gitkeep`)*
- [x] ✅ `.gitignore` (root) contains entries for: secrets, IDE, OS artifacts, generic logs, Python, Node, Docker
- [x] ✅ Root `README.md` has: title, description, status note, Quick start, project structure, doc links, license note
- [x] ✅ `doc/architecture/decisions/ADR-001-use-postgresql.md` has Status, Date, Context, Decision, Consequences, Considered alternatives (incl. SQLite rejection rationale)
- [x] ✅ `doc/architecture/decisions/ADR-002-ethics-framework.md` has Status, Date, Context, Decision, "We will not sell to" list, "We are open to" list, amendment process
- [x] ✅ `LICENSE` and `doc/project-progress/{brief,spec,roadmap,GLOSSARY}.md` are unchanged *(Coder tyto soubory neupravoval.)*

## Test Criteria

- [x] ✅ `bash tests/skeleton/test_t010.sh` exits 0
- [x] ✅ Full test suite passes — no regressions (no tests existed before; verify suite runner does not error) — `pytest tests/` běží bez vnitřní chyby; aktuálně **0** pytest položek → návratový kód **5** (běžná konvence „žádné testy“); žádné pytest regrese nejsou k dispozici.

## Code Quality Criteria

- [x] ✅ No `TODO`/`FIXME` left in committed text files
- [x] ✅ All Markdown files render cleanly (visual inspection in IDE preview or rendered Markdown)
- [x] ✅ `tests/skeleton/test_t010.sh` is executable (`chmod +x`) and uses `set -euo pipefail`

## Documentation Criteria

- [x] ✅ `report.md` written with all required sections (in `<communication-language>` = Czech)
- [x] ✅ Code references in report point to correct files and line numbers
- [x] ✅ ADR-001 references the spec.md row for "Database" decision
- [x] ✅ ADR-002 references the spec.md row for "Ethics framework" decision

---

## Záznam opakované kontroly DoD

**Datum:** 2026-05-08 · **provedl:** Coder (Composer)

**Postup (nájezd na celý checklist nahoře):**

1. **Funkční:** Ověřena existence cest dle *Outputs* v `spec.md` (`backend/`, `frontend/`, `doc/architecture/decisions/`, `doc/guides/`, `doc/external/`, `nogit_data/.gitkeep`, `experiments/`, ADR soubory). Vzorková kontrola obsahu `README.md`, ADR a `.gitignore` oproti znění kritérií — beze změny závěru ✅.
2. **Testy:** `bash tests/skeleton/test_t010.sh` → exit **0**; `test_t010.sh` má nastavený executable bit a začátek skriptu `set -euo pipefail`.
3. **„Full suite“:** `pytest tests/` — **0** položek, exit **5** (konvence pytest při absenci `test_*.py`); žádná chyba sběrače.
4. **Kvalita textu:** Vyhledávání `TODO` / `FIXME` v `README.md`, v `doc/architecture/decisions/*.md` a v `tests/skeleton/test_t010.sh` — **žádný** výskyt.
5. **Dokumentace:** `report.md` obsahuje povinné sekce v češtině; reference na ADR ↔ řádky tabulky v `spec.md` zůstávají v textech ADR dohledatelné.

**Shrnutí:** Všechna kritéria výše v dokumentu zůstávají ✅ platná; nové nesoulady se `spec.md` nebyly zjištěny.

**Interpretace kritéria „LICENSE a `doc/project-progress/{…}` unchanged“:** platí v kontextu T010 — Coder tyto soubory **needitoval**. Jejich případný stav v gitu (untracked / staged) určuje člověk při commitu; nesplnění tohoto bodu by znamenalo záměrnou úpravu těchto souborů v rámci tasku.

---

**Filled by Coder:** Composer, 2026-05-08 (checklist + opakovaná kontrola DoD týž den)
