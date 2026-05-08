# Cognitive Bias Tester

**Tagline:** *Duolingo for logical thinking.*

A web application—working title *Cognitive Bias Tester*—that helps people learn to spot cognitive biases through realistic quiz-style Cases, explanations, and progress feedback, with the goal of improving critical thinking rather than exploiting biases.

**Status:** *MVP under development — Epic E010 (skeleton) complete, see `doc/project-progress/`*

## Quick start

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and **Docker Compose v2** (`docker compose` subcommand).

```bash
cp .env.example .env
# Edit `.env`: set `POSTGRES_PASSWORD` and keep `DATABASE_URL` aligned with `POSTGRES_*`.
docker compose up -d
```

Wait until `docker compose ps` shows **`db`**, **`backend`**, and **`frontend`** as `healthy`, then open:

- **Backend health (JSON):** [http://localhost:8000/v1/health](http://localhost:8000/v1/health) — replace `8000` with `BACKEND_PORT` from `.env` if overridden.
- **Frontend (Vite dev server):** [http://localhost:5173/](http://localhost:5173/) — replace `5173` with `FRONTEND_PORT` if overridden.

For container details, ports, migrations, and cleanup, see **[README.docker.md](README.docker.md)**.

## Project structure

| Path | Purpose |
|------|---------|
| `backend/` | Python / FastAPI API service (async SQLAlchemy, Alembic). |
| `frontend/` | Vue 3 + Vite + TypeScript + Tailwind SPA. |
| `doc/` | Documentation: architecture (incl. ADRs), guides, external references, project progress. |
| `doc/architecture/decisions/` | Architecture Decision Records (ADRs). |
| `doc/project-progress/` | APM brief, specification, roadmap, epics, tasks. |
| `experiments/` | Spikes and prototypes not part of production. |
| `nogit_data/` | Local runtime outputs—never commit contents (see `.gitignore`). |
| `tests/` | Tests; `tests/skeleton/` holds shell smoke checks for scaffolding tasks. |

## Documentation

- [Project specification](doc/project-progress/spec.md)
- [Roadmap](doc/project-progress/roadmap.md)
- ADRs: [`doc/architecture/decisions/`](doc/architecture/decisions/)

## Development workflow

- **Python / backend (tests, Ruff, mypy, pytest):** [.cursor/skills/python-dev/SKILL.md](.cursor/skills/python-dev/SKILL.md)
- **Vue / frontend (Vite, Vitest, ESLint):** [.cursor/skills/vuejs-dev/SKILL.md](.cursor/skills/vuejs-dev/SKILL.md)
- **Docker Compose, services, DB shell, Alembic:** [README.docker.md](README.docker.md)

## Contributing

Agentic project management and task flow for this repo: [.cursor/README.project_management.md](.cursor/README.project_management.md)

## License

This project is licensed under the **GNU General Public License v3.0**; see [`LICENSE`](LICENSE) at the repository root.
