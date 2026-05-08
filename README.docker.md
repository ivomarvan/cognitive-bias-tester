# Docker usage — Cognitive Bias Tester

Infrastructure and application containers for local development. Production-oriented image targets exist for **`backend`** and **`frontend`**; Compose uses the **`dev`** targets by default with bind mounts for hot reload.

## Quick start

From the repository root:

```bash
cp .env.example .env
# Edit `.env` — at minimum set `POSTGRES_PASSWORD` and keep `DATABASE_URL` in sync
# with `POSTGRES_*` (see `.env.example`).
docker compose up -d
```

Wait until `docker compose ps` shows **`db`**, **`backend`**, and **`frontend`** as `healthy`, then use the URLs from the root [README.md](README.md) or the tasks below.

**Startup order:** `backend` waits until `db` is healthy; `frontend` waits until `backend` is healthy (see `depends_on` in `docker-compose.yml`).

To stop containers (default named volumes are kept):

```bash
docker compose down
```

## Services

Host ports come from `.env` (`POSTGRES_PORT`, `BACKEND_PORT`, `FRONTEND_PORT`). Defaults below match `.env.example`.

| Service | Port (host) | Description | Healthcheck |
|---------|-------------|-------------|-------------|
| `db` | `${POSTGRES_PORT:-5433}` → `5432` in container | PostgreSQL **16.2** (`postgres:16.2-alpine`); data in volume `postgres_data`. | `pg_isready -U $POSTGRES_USER -d $POSTGRES_DB` |
| `backend` | `${BACKEND_PORT:-8000}` → `8000` | FastAPI + Uvicorn (`./backend`, target **dev** by default). | `curl -f http://localhost:8000/v1/health` |
| `frontend` | `${FRONTEND_PORT:-5173}` → `5173` | Vue 3 + Vite dev server (`./frontend`, target **dev**); `src/` bind-mounted. | `wget -q --spider http://localhost:5173/` |

All services use `restart: unless-stopped` and read configuration from `.env` / Compose variable substitution. There is no custom `networks:` block; the default Compose network is used.

## Development vs production images

Compose builds **dev** images so you can edit code on the host with reload/HMR.

To build **production** images explicitly (no Compose service defined for these targets — run for release checks or external orchestration):

```bash
# Backend: lean image, non-root user, embedded app (no bind mounts)
docker compose build backend --target production

# Frontend: static `dist/` served by nginx (non-root, listens on 8080 in image)
docker compose build frontend --target production
```

Default **dev** builds (what `docker compose build` uses given `target: dev` in `docker-compose.yml`):

```bash
docker compose build backend
docker compose build frontend
```

## Troubleshooting

### `Bind for 0.0.0.0:5432 failed: port is already allocated`

Something on the host may already use a port. Set **`POSTGRES_PORT`**, **`BACKEND_PORT`**, or **`FRONTEND_PORT`** in `.env` to free host ports. Inside the stack, services still reach Postgres at host **`db`**, port **5432**.

## Common tasks

### Hit the API health endpoint

```bash
curl -s "http://127.0.0.1:${BACKEND_PORT:-8000}/v1/health"
```

### Open the Vite dev UI (landing page)

Browser: `http://127.0.0.1:${FRONTEND_PORT:-5173}/`

### Open `psql` inside the database container

```bash
docker compose exec db psql -U "${POSTGRES_USER:-cbt_app}" -d "${POSTGRES_DB:-cognitive_bias_tester}"
```

(Replace with values from your `.env` if they differ.)

### Run backend tests

With `db` and `backend` up (or using a one-off run that has DB access):

```bash
docker compose exec backend pytest
docker compose exec backend pytest -m unit
docker compose exec backend pytest -m integration tests/test_db.py
```

### Run Alembic migrations (`backend` container)

```bash
docker compose exec backend alembic upgrade head
```

Rollback all migrations:

```bash
docker compose exec backend alembic downgrade base
```

### Add a frontend npm dependency

Rebuild after changing `package.json` / lockfile:

```bash
docker compose exec frontend npm install <package-name>
docker compose build frontend
docker compose up -d frontend
```

Or edit `frontend/package.json` on the host, then `docker compose build frontend && docker compose up -d frontend`.

### Remove containers **and** the Postgres volume (destructive)

`docker compose down -v` deletes the named volume **`postgres_data`** and **all database data**. Use only when you intend to reset the local DB from scratch.

### Periodic cleanup (disk usage)

Per project Docker policy:

```bash
docker system prune -f
docker volume prune -f
```

Review output before running in shared environments — prunes unused images, containers, networks, and (for `volume prune`) unused volumes.
