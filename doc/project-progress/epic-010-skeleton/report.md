---
apm_category: epic-report
apm_ref: E010
apm_level: epic
created_by: Coder
model: claude-sonnet-4-6
intended_for: Human, Planner
created_at: 2026-05-09
updated_at: 2026-05-09
---

# Epic Report: E010 — Repo & Infrastructure Skeleton

## Shrnutí epiky

V rámci E010 byl postaven kompletní, produkčně konfigurovatelný skelet projektu: Docker Compose prostředí se třemi zdravými službami (`db` PostgreSQL 16, `backend` FastAPI, `frontend` Vue 3 + Vite), async SQLAlchemy session s Alembic, přísná quality gate (ruff + mypy `--strict` + pytest na backendu, ESLint + vue-tsc + Vitest na frontendu), CI pipeline pro GitHub Actions, finální `README.md` a `README.docker.md`, a dvě Architecture Decision Records (ADR-001 PostgreSQL, ADR-002 etický rámec). Po uzavření E010 neexistuje žádná business logika — ta začíná v E020.

---

## Dokončené tasky

| Task | Název | Výsledek |
|------|-------|----------|
| T010 | Project structure, `.gitignore`, README skeleton, ADR-001 + ADR-002 | ✅ |
| T020 | Docker Compose se službou `db` + `.env.example` + `README.docker.md` draft | ✅ |
| T030 | Backend FastAPI skeleton + `/v1/health` + ruff/mypy/pytest | ✅ |
| T040 | Backend DB session + Alembic init | ✅ |
| T050 | Frontend Vue 3 + Vite + Tailwind skeleton + ESLint/Vitest | ✅ |
| T060 | Full-stack integration + finální `README.md` a `README.docker.md` | ✅ |
| T070 | CI pipeline (GitHub Actions) | ✅ |

---

## Klíčová rozhodnutí a poznatky

**Verze závislostí — přesné piny místo `^` rozsahů.**
Coder zvolil v `frontend/package.json` přesné verze (bez `^`) s `package-lock.json`, čímž zajistil reprodukovatelné buildy. Původní dod zmiňoval `^`; Coder výsledek zdůvodnil a Planner souhlasí — přístup je v souladu se spec T050 (výraz „pinned") i `10-python.mdc` analogií.

**PostgreSQL port 5433 jako výchozí (ne 5432).**
`.env.example` mapuje host port 5433 → kontejner 5432, aby se předešlo kolizi s lokálním Postgresem vývojáře. `README.docker.md` tuto skutečnost dokumentuje. Praktické rozhodnutí bez dopadu na produkci.

**ReDoc pin na `redoc@2.1.3`.**
Výchozí CDN tag `redoc@next` na jsDelivr občas vrací 404. Coder přidal vlastní `/redoc` route s pevnou verzí. Netýká se produkčního chování API — jen vývojářského pohodlí.

**Alembic: `asyncpg` → `psycopg` konverze pro offline migrace.**
`alembic/env.py` obsahuje helper `_sync_url_for_offline()`, který přepíše URL pro offline (SQL-emit) režim. Umožní budoucí dry-run migrace bez živého DB spojení.

**T050 report retroaktivně doplněn.**
Spec T050 obsahoval constraint `Files NOT to modify: doc/**`, který Coder interpretoval tak, že nezaloží `report.md` pod `doc/`. Dokument byl doplněn zpětně na pokyn Humana. Výsledek T050 (frontend) je plně funkční — šlo o dokumentační schodek, ne implementační.

**`.github/workflows/ci.yml` čeká na první push Humana.**
Coder T070 záměrně nepushoval — CI bude aktivní až po prvním `git push` od Humana na GitHub. `actionlint` prošel lokálně přes Docker image `rhysd/actionlint:1.7.3` (exit 0).

**Licence: GPLv3, ne MIT.**
Spec zmiňuje MIT jako příklad; skutečný soubor `LICENSE` je GNU GPL v3. `README.md` i `README.docker.md` uvádějí GPLv3 v souladu s obsahem souboru. Pokud je tato licence záměrná, žádná akce není potřeba.

---

## Odchylky od Epic Planu

| Odchylka | Popis | Dopad |
|----------|-------|-------|
| T050 bez `report.md` při odevzdání | Viz výše — constraint v spec. Doplněno zpětně. | Nulový na kód; dokumentační prodleva. |
| PostgreSQL default port 5433 místo 5432 | `.env.example` a `README.docker.md` volí 5433 pro výchozí host mapping. | Drobný rozdíl od spec T020 (spec říká 5432). Nepůsobí problémy v CI ani produkci. |
| Frontend nginx port 8080 v production stage | `Dockerfile` production stage spouští nginx na portu 8080, ne 5173. | Správné chování — 5173 je Vite dev port; nginx v prod má vlastní port. Žádný problém. |
| CI `actionlint` přes Docker (ne nativně) | Lokální binárka nebyla k dispozici; verifikace přes `docker run rhysd/actionlint:1.7.3`. | Ekvivalentní výsledek; exit 0. |

---

## Doporučení pro Planner

**1. Git stav před E020: zbývají necommitované soubory.**
`git status` ukazuje, že `.github/` (CI workflow), `new_planner.md`, T050 `report.md`, T070 `report.md` jsou dosud necommitovány, a T050 + T070 `dod.md` jsou lokálně modifikované. Human by měl tyto soubory commitovat a pushovat na GitHub, aby CI pipeline poprvé proběhl, než začne E020.

**2. Licence — potvrdit záměr.**
Pokud je GPLv3 záměrná volba, žádná akce není potřeba. Pokud jde o omyl a projekt měl být MIT nebo jiná licence, je vhodné to opravit ještě před E020, protože GPLv3 má copyleft dopady pro budoucí komercionalizaci (Stripe, B2B).

**3. E020 — datový model má přímou závislost na definici Případu.**
E020 tvoří doménové entity (`Case`, `CaseTranslation`, `BiasType`, `Rating`, `User`, `AnswerEvent`, `Subscription`). Klíčové pro Planner: parametrická struktura Případu (placeholdery `{currency_amount_small}`, `{local_first_name}`) musí být navržena jako součást schématu již v E020, protože ji v E030 (LLM pipeline) a E040 (frontend) využívá více komponent. Změna schématu po E030 by vyžádala novou migraci.

**4. E020 zahrnuje side-task s nízkou prioritou.**
Spec E020 zmiňuje „informální kontakt s katedrou psychologie FF UK / FSS MUNI". Tento side-task nemá vliv na MVG gate E020 a nevyžaduje vlastní Task Specification — postačí poznámka v Epic Planu E020.

**5. ADR-003 a ADR-004 jsou blokující pro E030.**
E030 (LLM Pipeline) nemůže začít bez rozhodnutí o LLM provideru (ADR-003) a embedding modelu (ADR-004). Planner by měl připravit srovnávací tabulku (OpenAI vs Anthropic vs Gemini, cost projection) jako součást Epic Planu E030, nikoli až za běhu implementace.

---

## Reference

- Epic Plan: [plan.md](plan.md)
- Task Reports:
  - [T010](task-010-project-structure/report.md)
  - [T020](task-020-docker-compose-db/report.md)
  - [T030](task-030-backend-skeleton/report.md)
  - [T040](task-040-backend-db-alembic/report.md)
  - [T050](task-050-frontend-skeleton/report.md)
  - [T060](task-060-integration-readme/report.md)
  - [T070](task-070-ci-pipeline/report.md)
