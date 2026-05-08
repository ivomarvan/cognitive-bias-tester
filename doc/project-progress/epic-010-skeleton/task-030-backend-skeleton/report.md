---
apm_category: task-report
apm_ref: E010.T030
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Report: E010.T030 — Backend FastAPI skeleton + `/v1/health` + ruff/mypy/pytest

---

## Co bylo implementováno

- Služba **`backend/`**: vícefázový `Dockerfile` (builder → dev s nástroji → production jako non-root), `.dockerignore`, `pyproject.toml` s pinovanými závislostmi, přísným `mypy`, `ruff` a `pytest` (markery `unit` / `integration` / `slow`, `asyncio` režim).
- FastAPI aplikace: `lifespan` jako zástupce bez I/O, `FastAPI(..., version=settings.VERSION)`, router z `src/api/health.py` — `GET /v1/health` s modelem `HealthResponse` a konfigurací přes `Settings` v `src/core/config.py`.
- Základní logování v `src/core/logging.py` (strukturovaný formát, úroveň z nastavení).
- Testy `backend/tests/test_health.py`: `@pytest.mark.unit`, `httpx` přes `ASGITransport` — 200 + tvar JSON; 404 na neexistující cestě.
- **`docker-compose.yml`**: služba `backend` (`build` → target `dev`), `depends_on: db` se `service_healthy`, healthcheck `curl` na `/v1/health`, bind-mount `src` (a `tests` pro dev image), příkaz `uvicorn` s `--reload`.
- Kořenový **`README.docker.md`**: quick start včetně `db` + `backend`, porty a příklad `curl` na health.
- Regresní skript **`tests/skeleton/test_t030.sh`**: `docker compose config`, build, v kontejneru `ruff` + `mypy` + `pytest -m unit`; volitelně stack s přemapovanými porty (`POSTGRES_PORT` / `BACKEND_PORT`) a kontrola HTTP z hostitele.

---

## Vstupy a výstupy

### Přečteno

- `doc/project-progress/epic-010-skeleton/task-030-backend-skeleton/spec.md`
- `doc/project-progress/epic-010-skeleton/task-030-backend-skeleton/dod.md`
- `.cursor/rules/04-docker-standards.mdc` (relevantní části)
- `.cursor/rules/10-python.mdc`
- `.cursor/rules/14-fastapi.mdc`
- `docker-compose.yml` a `.env.example` z T020

### Vytvořeno

- `backend/Dockerfile`
- `backend/.dockerignore`
- `backend/pyproject.toml`
- `backend/src/__init__.py`
- `backend/src/main.py`
- `backend/src/api/__init__.py`
- `backend/src/api/health.py`
- `backend/src/core/__init__.py`
- `backend/src/core/config.py`
- `backend/src/core/logging.py`
- `backend/tests/__init__.py`
- `backend/tests/test_health.py`
- `tests/skeleton/test_t030.sh`
- `doc/project-progress/epic-010-skeleton/task-030-backend-skeleton/report.md`

### Změněno

- `docker-compose.yml` (služba `backend`)
- `README.docker.md` (služby, start, health)
- `tests/skeleton/test_t010.sh` (po odstranění `backend/.gitkeep` kontrola `backend/.gitkeep` **nebo** `backend/pyproject.toml`)
- `doc/project-progress/epic-010-skeleton/task-030-backend-skeleton/dod.md`

### Nedotčeno (Context Bundle)

- `frontend/`
- `nogit_data/`
- `experiments/`
- `doc/project-progress/brief.md`
- `doc/project-progress/spec.md`
- `doc/project-progress/roadmap.md`
- `doc/project-progress/GLOSSARY.md`
- ostatní taskové složky epiky kromě vlastního `task-030-backend-skeleton/**` aktualizovaného artefaktům tasku
- `.cursor/**`
- `LICENSE`
- kořenový `README.md` (dle T060)

---

## Použité metody a rozhodnutí

### Multi-stage image a dev vs. production

Builder instaluje runtime závislosti do prefixu; `dev` přidává `[dev]` (ruff, mypy, pytest, httpx) a `curl` pro Compose healthcheck. Production kopíruje jen `src/`, běží jako `appuser`, vlastní `HEALTHCHECK` a `uvicorn` přes `python -m`.

### Konfigurace a verze API

Jednotný zdroj pravdy: `Settings` (`pydantic-settings`), `.env` přes `SettingsConfigDict`. Pole `version` u `FastAPI` se bere z `settings.VERSION` (ne duplicitní literál v kódu routeru).

### Docker Compose a testy na hostiteli

Aby se předešlo kolizím s lokálním Postgresem a jiným API na **8000**, skript `test_t030.sh` nastavuje např. `POSTGRES_PORT=15432` a `BACKEND_PORT=18080`. K dev image se mountuje i `./backend/tests`, protože `.dockerignore` vylučuje `tests/` z kontextu buildu — bez svazku by `pytest` v kontejneru nenašel soubory.

### `pytest-asyncio`

V `[tool.pytest.ini_options]` je `asyncio_default_fixture_loop_scope = "function"`, aby odpadla deprecation warning při `async` testech.

### APM dokumentace v `doc/**`

Checklist `dod.md` a tento `report.md` leží pod `doc/project-progress/...`; stejný vzor jako u T010/T020 doplňuje povinné APM výstupy tasku.

---

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `backend/Dockerfile` | 1-37 | Tři stage (`builder`, `dev`, `production`), pin `python:3.12.3-slim`, non-root + HEALTHCHECK v produkci. |
| `backend/.dockerignore` | 1-12 | Cache, testy, `.env`, `.git` mimo build kontext. |
| `backend/pyproject.toml` | 1-54 | Závislosti s komentáři, ruff/mypy/pytest včetně asyncio scope. |
| `backend/src/main.py` | 1-31 | `lifespan`, `FastAPI` s `version=settings.VERSION`, mount health routeru, `configure_logging`. |
| `backend/src/api/health.py` | 1-28 | `APIRouter` prefix `/v1`, `HealthResponse`, `GET /health` s Google docstringem. |
| `backend/src/core/config.py` | 1-19 | `Settings`, `settings` singleton, načítání `.env`. |
| `backend/src/core/logging.py` | 1-18 | `configure_logging`, formát logů. |
| `backend/tests/test_health.py` | 1-31 | Dva unit testy: 200 health, 404 default handler. |
| `docker-compose.yml` | 1-54 | Služby `db` a `backend` (healthcheck, závislost na healthy DB, volumes, uvicorn). |
| `tests/skeleton/test_t030.sh` | 1-74 | Kontejnerové quality gate + volitelný Docker run a `curl`. |
| `README.docker.md` | 1-61 | Dokumentace Compose včetně backendu a health endpointu. |
| `.env.example` | 1-20 | Šablona proměnných včetně `BACKEND_PORT` (T020 + použití T030). |

---

## Výsledek regresního testu

| Command / scope | Result | Notes |
|-----------------|--------|-------|
| `bash tests/skeleton/test_t010.sh` | ✅ exit **0** | Součást řetězce před dokončením tasku. |
| `bash tests/skeleton/test_t020.sh` | ✅ exit **0** | DB healthy, skript OK. |
| `bash tests/skeleton/test_t030.sh` | ✅ exit **0** | Build, ruff, mypy, `pytest -m unit`, volitelně stack + `curl` na `${BACKEND_PORT}/v1/health`. |
| `pytest tests/ -v --tb=short` (kořen) | ✅ exit **5**, **0** testů | Očekávané — unit testy žijí v `backend/tests/` a root `tests/` je především skeleton shell. |

---

## Definition of Done

Všechna kritéria v [dod.md](dod.md) jsou vyplněna jako splněná (✅), včetně poznámek k přemapování portů ve skriptu, mountu `tests/` v Compose a vnitřímu portu **8000** dle zadání.

---
