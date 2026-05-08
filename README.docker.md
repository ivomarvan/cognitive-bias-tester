# Docker usage — Cognitive Bias Tester

Infrastructure and application containers for local development and parity with production-style PostgreSQL.

## Quick start

From the repository root:

```bash
cp .env.example .env
# Edit `.env` — at minimum set `POSTGRES_PASSWORD` and keep `DATABASE_URL` in sync
# with `POSTGRES_*` (see `.env.example`).
docker compose up -d db backend
```

Wait until `docker compose ps` shows **`db`** (and **`backend`**) as `healthy`, then open the API or database (see **Common tasks**).

To stop:

```bash
docker compose down
```

## Services

| Service | Port (host) | Image / build | Description |
|---------|---------------|---------------|-------------|
| `db` | `${POSTGRES_PORT}` → `5432` in container (default host map **5433**) | `postgres:16.2-alpine` | PostgreSQL; data in named volume `postgres_data`. |
| `backend` | `${BACKEND_PORT}` → `8000` (default **8000**) | `./backend` (`target: **dev**`) | FastAPI + Uvicorn with `--reload`; source bind-mounted. |

**Note:** **frontend** service arrives in task T050. **`backend`** is introduced in T030 (FastAPI skeleton).

## Troubleshooting

### `Bind for 0.0.0.0:5432 failed: port is already allocated`

Something on the host is already using **5432** (often a system PostgreSQL). Set **`POSTGRES_PORT`** in `.env` to a free port (the repo default in `.env.example` is **5433**), then `docker compose up -d db backend` again. Containers still talk to Postgres on hostname **`db`**, port **5432** inside the Docker network; only the host mapping changes.

## Common tasks

### Hit the API health endpoint

```bash
curl -s "http://127.0.0.1:${BACKEND_PORT:-8000}/v1/health"
```

### Open `psql` inside the database container

```bash
docker compose exec db psql -U "${POSTGRES_USER:-cbt_app}" -d "${POSTGRES_DB:-cognitive_bias_tester}"
```

(Replace with values from your `.env` if they differ.)

### Run Alembic migrations (`backend` container)

From the repo root (with `db` and `backend` up):

```bash
docker compose exec backend alembic upgrade head
```

Rollback all migrations:

```bash
docker compose exec backend alembic downgrade base
```

### Remove containers **and** the Postgres volume (destructive)

`docker compose down -v` deletes the named volume **`postgres_data`** and **all database data**. Use only when you intend to reset the local DB from scratch.

### Periodic cleanup (disk usage)

Per project Docker policy:

```bash
docker system prune -f
docker volume prune -f
```

Review output before running in shared environments — prunes unused images, containers, networks, and (for `volume prune`) unused volumes.
