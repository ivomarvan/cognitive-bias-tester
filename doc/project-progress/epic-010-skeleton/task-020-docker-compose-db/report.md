---
apm_category: task-report
apm_ref: E010.T020
apm_level: task
created_by: Coder
model: Composer
intended_for: Human
created_at: 2026-05-08
updated_at: 2026-05-08
---

# Task Report: E010.T020 — Docker Compose s `db`, `.env.example`, `README.docker.md`

---

## Co bylo implementováno

- Kořenový `docker-compose.yml` se službou **`db`**: PostgreSQL `postgres:16.2-alpine`, pojmenovaný volume `postgres_data`, mapování portu `${POSTGRES_PORT:-5432}:5432`, `restart: unless-stopped`, healthcheck `pg_isready` (interval 10 s, timeout 5 s, retries 5), bez pole `version:`.
- Soubor **`.env.example`** se všemi proměnnými ze zadání a jednořádkovými komentáři.
- **`README.docker.md`**: Quick start, tabulka služeb (pouze `db` + poznámka k T030/T050), běžné úkoly včetně psql, varování u `docker compose down -v` a periodic prune dle Docker policy.
- Spustitelný **`tests/skeleton/test_t020.sh`**: validace `docker compose config`, negativní test chybějícího `POSTGRES_PASSWORD`, kontrola absence `version:`, volitelně plný běh `up` / health / `down` (nebo `SKIP_DOCKER_RUN=1`).

---

## Vstupy a výstupy

### Přečteno

- `doc/project-progress/epic-010-skeleton/task-020-docker-compose-db/spec.md`
- `doc/project-progress/epic-010-skeleton/task-020-docker-compose-db/dod.md`
- `.cursor/rules/03-docker-policy.mdc`
- `.cursor/rules/04-docker-standards.mdc`
- `.cursor/skills/docker-new-project/SKILL.md`
- Kořenový `.gitignore` (T010 — vyloučení `.env`)

### Vytvořeno

- `docker-compose.yml`
- `.env.example`
- `README.docker.md`
- `tests/skeleton/test_t020.sh`

### Změněno

- `doc/project-progress/epic-010-skeleton/task-020-docker-compose-db/dod.md`
- `doc/project-progress/epic-010-skeleton/task-020-docker-compose-db/report.md`

### Nedotčeno (Context Bundle)

- `.cursor/**`
- `doc/**` mimo artefakty tohoto tasku (`dod.md`, `report.md` v `task-020-docker-compose-db/`)
- `LICENSE`
- `backend/`, `frontend/`

---

## Použité metody a rozhodnutí

### `env_file` a chování bez souboru `.env`

Zadání vyžaduje napojení na `.env` a zároveň test bez přítomnosti projektového `.env`. Použit byl Compose long syntax `env_file` s `required: false`, takže chybějící `.env` na disku neblokuje `docker compose --env-file <temp>` při interpolaci proměnných; hodnoty pro kontejner jsou předány přes blok `environment` s substitucí.

### Povinné heslo

`POSTGRES_PASSWORD` je v `docker-compose.yml` jako `${POSTGRES_PASSWORD:?…}` bez výchozí hodnoty; `docker compose config` končí chybou, pokud proměnná chybí (ověřeno v testu).

### Port ve skriptu T020

Na vývojářském stroji může být **5432** obsazené lokálním Postgresem. Test po vygenerování env z `.env.example` přepíše **`POSTGRES_PORT` na 15432**, aby selhání bindu nevedlo k falešně červenému testu — uživatelský postup z `README.docker.md` dál defaultuje na 5432 z `.env.example`.

---

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `docker-compose.yml` | 1-23 | Služba `db`, volume, healthcheck, interpolace env. |
| `.env.example` | 1-20 | Dokumentované proměnné pro Postgres a rezervované porty T030/T050. |
| `README.docker.md` | 1-54 | Quick start, služby, psql, `down -v`, `docker system/volume prune`. |
| `tests/skeleton/test_t020.sh` | 1-75 | Config, negace hesla, grep bez `version:`, volitelný Docker běh a health poll 30 s. |

---

## Výsledek regresního testu

| Command / scope | Result | Notes |
|-----------------|--------|-------|
| `bash tests/skeleton/test_t010.sh` | ✅ exit **0** | Kostra T010 beze změny chování. |
| `bash tests/skeleton/test_t020.sh` | ✅ exit **0** | `db` healthy; port testu **15432**. |
| `pytest tests/ -q` | ✅ exit **5** | 0 pytest položek (očekáváno). |

---

## Definition of Done

Shrnutí splnění kritérií je v [dod.md](dod.md) včetně poznámky k použití portu **15432** v integrační části T020 testu.
