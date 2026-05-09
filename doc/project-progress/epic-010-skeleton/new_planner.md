Handoff Planner role — Cognitive Bias Tester
1. Co je projekt
Webová aplikace „Duolingo pro logické myšlení" — testuje kognitivní zkreslení (Kahneman) na AI-generovaných příkladech. Tři módy (jednorázová otázka, komplexní test, sociální sítě). Klíčový strategický constraint: monetizace musí být ready před spuštěním Mód 3 (X).

Veškeré detaily jsou v souborech — plnou specifikaci si nový Planner přečte z disku, ne ode mě.

2. Souborová mapa pro nového Plannera (čti v tomto pořadí)
Pořadí	Soubor	Účel
1
.cursor/rules/00-communication-language.mdc
jazyk = cs (chat česky, kód anglicky)
2
.cursor/README.project_management.md
celý APM workflow + role Planner / Coder / Human
3
.cursor/rules/07-project-management.mdc
machine-readable APM konvence + YAML front matter + Security guards
4
.cursor/rules/01-general-programming.mdc, 02-git.mdc, 03-docker-policy.mdc, 06-project-structure.mdc
obecné pravidla projektu (always-applied)
5
.cursor/rules/{10-python, 11-vuejs-vite-tailwind, 13-sql-postgresql, 14-fastapi, 15-qdrant}.mdc
technologické rules
6
.cursor/skills/{project-init, plan-epic, execute-task, review-epic}/SKILL.md
čtyři APM fáze
7
doc/project-progress/GLOSSARY.md
terminologie APM (en/cs)
8
doc/project-progress/brief.md
původní zadání + hodnocení Gemini 3.1 Pro a Opus 4.7
9
doc/project-progress/spec.md
single source of truth projektu — Goal, Scope (E010–E130 Monetized MVP), Non-Goals, 15 Key Technical Decisions, Assumptions, Project-level DoD
10
doc/project-progress/roadmap.md
13 MVP epik + 7 post-MVP epik s Status / Complexity / Depends on / MVP gate
11
doc/project-progress/epic-010-skeleton/plan.md
aktivní Epic Plán + Cross-Task Conventions + 7 task specifikací
12
reporty Codera v epic-010-skeleton/task-NNN-*/report.md
co už bylo skutečně postaveno (T010, T020, T030, T040)
3. Role Plannera v APM (jednou větou)
Planner plánuje a píše dokumenty, neimplementuje produkční kód. Píše spec.md, roadmap.md, epic-NNN/plan.md, task-NNN/{spec,dod}.md a po každém Epicu reviewuje validitu roadmapy. Coder pak implementuje výhradně podle Plannerových dokumentů — pokud něco chybí nebo je nejasné, je to chyba Plannera.

Detailně viz .cursor/README.project_management.md (sekce „The Two Actors" → „Planner") a .cursor/rules/07-project-management.mdc.

4. Aktuální stav (k 8. 5. 2026, 18:25 SELČ)
Fáze APM:

F0 (Project Init): ✅ schváleno člověkem (F0.5 gate)
FE pro E010 (Epic Plan): ✅ schváleno člověkem (FE.2 gate)
FT pro tasky T010–T070: ⏳ probíhá, viz tabulka níže
FER pro E010: ⏸ ještě ne
Tasky E010 (Repo & Infrastructure Skeleton):

Task	Stav	Poznámka
T010 — T070 — Hotovo vyžaduje revizi

5. Klíčová strategická rozhodnutí, která Planner už udělal
Vše je v spec.md a roadmap.md, ale přehled pro orientaci:

Pořadí fází nedotknutelné: Foundation → Monetisation Ready → Server → Public + Viral. Mód 3 (X publishing) nesmí jít live před fungujícím Stripe v produkci.
5 bias typů v MVP: anchoring, framing, loss aversion, confirmation bias, sunk cost.
Two-tier UI překlad: Tier A (LLM cache, libovolný jazyk) pro Případy + mikrocopy; Tier B (human-curated, MVP cs+en) pro landing/legal/payment/brand.
Cena: 3,99 € global v MVP; PPP localizace („cena 2 piv") je E165 post-MVP.
B2B mimo MVP: žádný Contact-Sales formulář ani enterprise tier do E140+.
První síť: X / Twitter (single channel pro MVP launch).
Stack: PostgreSQL 16 v Dockeru, FastAPI (Python 3.12), Vue 3 + Vite + TS strict + Tailwind + Pinia, Stripe Checkout, magic link auth, hosting Render/Fly.io (ADR-005 v E090).
8 plánovaných ADR: ADR-001 (PG, hotové v T010), ADR-002 (etika, hotové v T010), ADR-003 (LLM provider — v E030), ADR-004 (embedding model — v E030), ADR-005 (hosting — v E090), ADR-006 (auth — v E050), ADR-007 (Stripe — v E060), ADR-008 (analytics — v E100).
Tabulka odložených rozhodnutí je v spec.md sekce „Key Technical Decisions" (ADR-003 až ADR-008 jsou explicitně vázány na konkrétní Epic).

6. Otevřené body, na které nový Planner narazí jako první
Nejbližší rozhodovací bod:

Spustit Phase ER (skill review-epic):
Coder napíše epic-010-skeleton/report.md agregující 7 task reportů.
Planner přečte Epic Report + roadmap + spec a navrhne jednu ze tří závěrů: roadmap unchanged / update / major revision.
Human rozhodne.
Pak začíná Phase E pro E020 (Data Model + Seed Cases) — to je první „opravdová" content práce: doménové entity (Case, CaseTranslation, Rating, User, BiasType, AnswerEvent, Subscription placeholder), Alembic migrace, 25 ručně napsaných gold-standard Case v angličtině pro 5 zkreslení × 5 variant. Side-task v E020: navázat informální kontakt s katedrou psychologie (FF UK / FSS MUNI).

E030 (LLM Pipeline & Cache) je nejnáročnější část MVP a Planner si ji bude muset dobře promyslet — ADR-003 (provider + cost projection), ADR-004 (embedding), prompt templates, LLM-as-judge validátor, deduplication threshold.

7. Bezpečnostní zábrany — Planner i Coder je dodržují
Žádný git commit/push/pull/merge/rebase/reset bez explicitního pokynu Humana.
Coder nikdy negitoví — Human review (FT.7) → Human commit.
Žádné DB migrace v produkci bez schválení.
Žádné destruktivní operace bez potvrzení.
Submodul .cursor/ se nikdy z projektu nemění (změny patří do upstream repa template).
8. Co konkrétně předat novému Plannerovi (prompt template)
Stačí, když novému agentovi řekneš něco ve stylu:

Přebíráš roli Planner v APM workflow. Projekt: cognitive-bias-tester. Začni přečtením souborů v tomto pořadí: 1. .cursor/README.project_management.md 2. .cursor/rules/00-communication-language.mdc + 07-project-management.mdc 3. doc/project-progress/{brief, spec, roadmap, GLOSSARY}.md 4. doc/project-progress/epic-010-skeleton/plan.md + všechny task reporty (T010–T040 už hotové) 5. git log --oneline a git status pro fyzický stav.

Aktuálně: T040 dokončen Coderem, čeká na FT.7 review. T050–T070 čekají. Po E010 jde Phase ER → E020.