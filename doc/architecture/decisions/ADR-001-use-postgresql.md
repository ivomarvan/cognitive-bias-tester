# ADR-001: Use PostgreSQL for the primary database

**Status**: Accepted

**Date**: 2026-05-08

## Context

The product stores user progress, Cases, LLM cache entries, ratings, and related metadata. The project specification (`doc/project-progress/spec.md`, **Key Technical Decisions** — row **3**, **Database**) commits to **PostgreSQL 16 in Docker** for development and production parity, with rationale including `JSONB` for flexible Case payload and optional full-text search.

We need concurrent access, durable ACID transactions, and a mature migration story as content and traffic grow. SQLite is attractive for local-only prototypes but becomes a bottleneck for multi-writer workloads and operational tooling shared across environments.

## Decision

Use **PostgreSQL 16** as the primary database, run locally via **Docker Compose**, and target the same major version in production so schema and query behavior match across environments.

## Considered alternatives

- **SQLite (file-backed)** — rejected for MVP: single-writer semantics and limited concurrency under web traffic; weaker fit for multi-instance API deployments and background workers. Acceptable for disposable experiments, not for the main application store cited in `spec.md` row 3.
- **Managed MySQL/MariaDB** — viable, but the team standard and documented project decision center on PostgreSQL 16; switching would require revisiting JSON/query assumptions and training cost without clear benefit for this codebase.

## Consequences

- **Positive:** Strong concurrency, rich SQL + `JSONB`, battle-tested migration tooling (e.g. Alembic), and alignment with `spec.md` / infrastructure choices.
- **Negative:** Local developers must run Docker (or an equivalent Postgres instance), which is already mandated by project Docker policy for multi-service work.
