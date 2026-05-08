---
apm_category: task-report
apm_ref: E010.T040
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Report: E010.T040 — Backend DB session + Alembic init

---

## Co bylo implementováno

- **`src/db/session.py`**: asynchronní `create_async_engine` (`pool_pre_ping`, `pool_size` z `Settings`), `async_sessionmaker`, FastAPI dependency `get_session` s návratovým typem **`AsyncGenerator[AsyncSession, None]`** (soulad s `16-sqlalchemy.mdc`); modulový logger po inicializaci enginu.
- **`src/db/base.py`**: `DeclarativeBase` jako **`Base`** pro budoucí ORM modely (výhradně styl 2.x — `Mapped` / `mapped_column` až v dalších úkolech).
- **`src/db/models/__init__.py`**: balíček pro entity; místo pro importy modelů tak, aby se při **`alembic revision --autogenerate`** naplnilo **`Base.metadata`** (zatím bez konkrétních tabulek — T040 záměrně bez business schématu).
- **`alembic`**: `alembic.ini`, `script.py.mako`, `env.py` s online migracemi (`async_engine_from_config` + `connection.run_sync(do_run_migrations)`); offline převod `postgresql+asyncpg` → `postgresql+psycopg`; **`target_metadata = Base.metadata`** a import `src.db.models` (side-effect); prázdná revize **`0001`**.
- **`Settings`**: povinné `DATABASE_URL`, výchozí `DB_POOL_SIZE`; **`main.py` lifespan**: `SELECT 1`, při chybě `logger.exception`, shutdown `await engine.dispose()`.
- **`main.py` — ReDoc**: vestavěný `/redoc` vypnut (`redoc_url=None`); vlastní route s **`get_redoc_html`** a **přibitým** `redoc@2.1.3` na jsDelivr (výchozí `redoc@next` často 404).
- **Závislosti** (`pyproject.toml`): pinované `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `psycopg[binary]`; plugin **`pydantic.mypy`**; u **Ruffu** **`exclude`** pro `build`, `dist`, `.eggs` (po `pip install .[dev]` jinak vzniká `build/lib/…` a selhává `ruff format --check .` v kontejneru).
- **Compose**: u **`backend`** blok **`environment`** (`DATABASE_URL`, `DB_POOL_SIZE`); u **`db`** healthcheck **`pg_isready`** s **`-d "${POSTGRES_DB}"`**, aby nevznikaly falešné logy „database \<user\> does not exist“.
- **Testy / skripty**: `backend/tests/test_db.py`; `tests/skeleton/test_t040.sh`; `test_t030.sh` rozděleno (lint/typecheck `--no-deps`, unit s naběhnutým `db`); `test_t010.sh` — klíčové slovo licence **GNU General Public License**.
- **Dokumentace provozu**: `README.docker.md` — `DATABASE_URL`, Alembic příkazy; kořenový `README.md` — licence GPLv3 (shoda s `LICENSE`).

---

## Vstupy a výstupy

### Přečteno

- `doc/project-progress/epic-010-skeleton/task-040-backend-db-alembic/spec.md`
- `doc/project-progress/epic-010-skeleton/task-040-backend-db-alembic/dod.md`
- `.cursor/rules/13-sql-postgresql.mdc` (relevantní části)
- `.cursor/rules/16-sqlalchemy.mdc` (session, `Base`, Alembic metadata, dotazovací styl do budoucna)
- `.cursor/skills/postgresql-dev/SKILL.md` (sekce Alembic)
- Předchozí výstupy T020/T030

### Vytvořeno

- `backend/src/db/__init__.py`
- `backend/src/db/base.py`
- `backend/src/db/session.py`
- `backend/src/db/models/__init__.py`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/0001_initial.py`
- `backend/tests/test_db.py`
- `tests/skeleton/test_t040.sh`
- `doc/project-progress/epic-010-skeleton/task-040-backend-db-alembic/report.md`

### Změněno

- `backend/src/main.py`
- `backend/src/core/config.py`
- `backend/pyproject.toml`
- `backend/Dockerfile`
- `docker-compose.yml`
- `.env.example`
- `README.docker.md`
- `README.md`
- `tests/skeleton/test_t030.sh`
- `tests/skeleton/test_t010.sh`
- `doc/project-progress/epic-010-skeleton/task-040-backend-db-alembic/dod.md`
- `.env` *(lokální — doplnění `DATABASE_URL` / `DB_POOL_SIZE` po šabloně; typicky mimo git)*

### Nedotčeno (Context Bundle)

- `frontend/**`
- `LICENSE`
- `doc/project-progress/brief.md`
- `doc/project-progress/spec.md`
- `doc/project-progress/roadmap.md`
- `doc/project-progress/GLOSSARY.md`
- `doc/architecture/**` (bez úprav v rámci T040)
- jiné taskové složky než `task-040-backend-db-alembic/**`
- `backend/src/api/health.py`
- `.cursor/**` *(obsah submodulu se v tomto reportu neupravoval)*

---

## Použité metody a rozhodnutí

### Proč `environment` u `backend` v Compose

Skeleton skripty používají dočasný `--env-file` odvozený z `.env.example`. Bez předání `DATABASE_URL` do procesu kontejner Pydantic při importu `Settings` neuspěje. Explicitní `environment:` s interpolací `${DATABASE_URL:?…}` zajistí konzistentní chování u `compose run` i `up`.

### Proč unit testy potřebují `db`

`lifespan` ověřuje připojení k DB; ASGI testy health endpointu spouští startup. Proto `pytest -m unit` v `test_t030`/`test_t040` běží přes `docker compose run` **bez** `--no-deps`.

### Mypy a `Settings()`

Plugin **`pydantic.mypy`** řeší strict kontrolu u `Settings()` načítaných z prostředí.

### Zarovnání s `16-sqlalchemy` po merge submodulu

- **`Base`** + **`target_metadata = Base.metadata`** připravují **`alembic revision --autogenerate`**; prázdná revize T040 zůstává v platnosti.
- **`get_session`** jako **`AsyncGenerator`** odpovídá příkladům v pravidle.
- **`Ruff exclude`** řeší artefakty setuptools po buildu uvnitř `/app` — není rozpor s pravidlem, jen praktická úprava CI/quality gate.

### ReDoc

Třetí strana (jsDelivr `redoc@next`) je nestabilní; pinning **`redoc@2.1.3`** přes vlastní `/redoc` route obnoví funkční dokumentaci.

---

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `backend/src/db/base.py` | 1-7 | `DeclarativeBase` jako `Base`. |
| `backend/src/db/models/__init__.py` | 1-9 | Balíček modelů + návod na importy pro Alembic. |
| `backend/src/db/session.py` | 1-48 | Engine, `async_sessionmaker`, `get_session` (`AsyncGenerator`). |
| `backend/src/db/__init__.py` | 1-6 | Re-export `Base`, `engine`, `async_session`, `get_session`. |
| `backend/src/main.py` | 1-66 | Lifespan DB check, FastAPI app, vlastní `/redoc` s pinovaným JS. |
| `backend/src/core/config.py` | 1-22 | `DATABASE_URL`, `DB_POOL_SIZE`. |
| `backend/alembic/env.py` | 1-81 | `Base.metadata`, import `src.db`, async/offline migrace. |
| `backend/alembic/versions/0001_initial.py` | 1-14 | Prázdná revize `0001`. |
| `backend/pyproject.toml` | 1-64 | DB deps, `pydantic.mypy`, Ruff `exclude`. |
| `backend/Dockerfile` | 1-40 | Dev + production: `alembic` + zdrojáky. |
| `backend/tests/test_db.py` | 1-19 | Integrace `SELECT 1`. |
| `docker-compose.yml` | 1-58 | `backend.environment`; `db` healthcheck s `-d POSTGRES_DB`. |
| `.env.example` | 1-27 | Šablona včetně `DATABASE_URL`. |
| `README.docker.md` | 1-82 | Quick start, Alembic, troubleshooting. |
| `tests/skeleton/test_t040.sh` | 1-86 | Regresní skript T040. |

---

## Výsledek regresního testu

| Command / scope | Result | Notes |
|-----------------|--------|-------|
| `bash tests/skeleton/test_t010.sh` | ✅ exit **0** | GPLv3 klíčové slovo v `README.md`. |
| `bash tests/skeleton/test_t020.sh` | ✅ exit **0** | — |
| `bash tests/skeleton/test_t030.sh` | ✅ exit **0** | Unit se `db`; ruff/mypy včetně `alembic/env.py`. |
| `bash tests/skeleton/test_t040.sh` | ✅ exit **0** | Alembic upgrade / integration / downgrade / upgrade. |
| `pytest tests/` (kořen) | ⚪ **0** testů / exit **5** | Python testy v `backend/tests/`. |

---

## Definition of Done

Všechna kritéria v [dod.md](dod.md) jsou vyplněna jako splněná (✅).

---
