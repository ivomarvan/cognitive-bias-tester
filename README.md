# Cognitive Bias Tester

A web application—working title *Cognitive Bias Tester*—that helps people learn to spot cognitive biases through realistic quiz-style Cases, explanations, and progress feedback, with the goal of improving critical thinking rather than exploiting biases.

**Status:** MVP under development.

## Quick start

Full Docker-based services are introduced in later epics; the intended local workflow will be:

```bash
cp .env.example .env && docker compose up
```

*(`.env.example` and `docker-compose.yml` will appear as subsequent project tasks land.)*

## Project structure

| Path | Purpose |
|------|---------|
| `backend/` | Python / FastAPI service (skeleton). |
| `frontend/` | Vue 3 + Vite + TypeScript + Tailwind app (skeleton). |
| `doc/` | Documentation: architecture (incl. ADRs), guides, external references, project progress. |
| `doc/architecture/decisions/` | Architecture Decision Records (ADRs). |
| `doc/project-progress/` | APM brief, specification, roadmap, epics, tasks. |
| `experiments/` | Spikes and prototypes not part of production. |
| `nogit_data/` | Local runtime outputs—never commit contents (see `.gitignore`). |
| `tests/` | Tests; `tests/skeleton/` holds shell checks for early scaffolding tasks. |

## Further reading

- [Project specification](doc/project-progress/spec.md)
- [Roadmap](doc/project-progress/roadmap.md)

## License

This project is released under the **MIT License**; see [`LICENSE`](LICENSE) at the repository root.
