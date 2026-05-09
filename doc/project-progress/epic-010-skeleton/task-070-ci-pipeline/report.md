---
apm_category: task-report
apm_ref: E010.T070
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Report: E010.T070 — CI pipeline (GitHub Actions)

## Co bylo implementováno

Přidán GitHub Actions workflow **`.github/workflows/ci.yml`**: čtyři joby (`backend-quality`, `backend-integration`, `frontend-quality`, `docker-build`) na **`ubuntu-24.04`**, akce pinované major verzí (`@v4` / `@v5` / `@v3`), **`concurrency`** s `cancel-in-progress`. Integrační job používá service container **`postgres:16.2-alpine`** s **`pg_isready`**. **`docker-build`** nastavuje **`DOCKER_BUILDKIT`**, **`actions/cache@v4`** pro adresář build cache a **`docker compose -f docker-compose.yml build`** s ne-tajnými proměnnými pro vyhodnocení Compose (`POSTGRES_PASSWORD`, `DATABASE_URL`). Soubor **`.github/CODEOWNERS`** obsahuje zástupný vlastník **`@OWNER`** s komentářem.

## Vstupy a výstupy

- **Přečteno:** `task-070-ci-pipeline/spec.md`, `dod.md`, `backend/pyproject.toml`, `frontend/package.json`, `docker-compose.yml`.
- **Vytvořeno:** `.github/workflows/ci.yml`, `.github/CODEOWNERS`, tento `report.md`.
- **Změněno:** `doc/project-progress/epic-010-skeleton/task-070-ci-pipeline/dod.md`.

## Použité metody a rozhodnutí

- **Spouštěče:** kromě výstupů specu (`push` na `main`, PR do `main`, `workflow_dispatch`) je v YAML i **`push` na `feature/**`** podle **Goal** v úvodu specu.
- **`backend-integration`** má **`needs: backend-quality`**, aby se po chybě lintu/typechecku nespouštěl Postgres zbytečně. **`docker-build`** závisí na třech testovacích jobech, aby se obrazy stavěly až po zelených kontrolách.
- **`mypy`:** příkaz přesně podle specu: `mypy src/ --strict` z adresáře `backend/` (bez `alembic/env.py`, který lokální skeleton dříve často zahrnoval).
- **`actionlint`:** na vývojovém stroji není nainstalovaný binárně; kontrola proběhla přes image **`rhysd/actionlint:1.7.3`** (`docker run … /repo/.github/workflows/ci.yml`) — **bez výstupu, exit 0**.

## Reference do kódu

- `.github/workflows/ci.yml:4-21` — `name`, `concurrency`, `on` (včetně `feature/**`), `permissions`.
- `.github/workflows/ci.yml:23-57` — job `backend-quality` (Python 3.12, Ruff, mypy, pytest bez integrace).
- `.github/workflows/ci.yml:59-100` — job `backend-integration` (Postgres service, Alembic, pytest integrace).
- `.github/workflows/ci.yml:102-136` — job `frontend-quality` (Node 22, npm ci, eslint, vue-tsc, vitest, build).
- `.github/workflows/ci.yml:138-163` — job `docker-build` (buildx, cache, `docker compose build`).
- `.github/CODEOWNERS:1-4` — zástupný `@OWNER`.

## Výsledek regresního testu

✅ `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` — OK (PyYAML).  
✅ Lokální `docker compose build` s proměnnými jako v jobu `docker-build` — OK.  
✅ `bash tests/skeleton/test_t060.sh` — OK.  
✅ `actionlint` (Docker `rhysd/actionlint:1.7.3`) — bez výstupu, exit 0.

## Definition of Done

Viz [dod.md](dod.md) — všechna kritéria ✅.

## Poznámka pro Humana (FT.7)

Workflow a CODEOWNERS jsou připravené k commitu a **pushi na GitHub**; Coder **nepushoval** žádnou větev. Po nasazení prosím nahraď **`@OWNER`** v `.github/CODEOWNERS` skutečným účtem nebo týmem.
