---
apm_category: task-dod
apm_ref: E030.T030
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Definition of Done: E030.T030 — Embedding Client + Deduplication Service

## ORM model + migration

- [ ] `backend/src/db/models/case_embedding.py` — `CaseEmbedding` model with `ARRAY(Float)` vector
- [ ] `backend/alembic/versions/0003_add_case_embedding.py` — migration creates table
- [ ] `alembic upgrade head` succeeds (run in Docker with live DB)
- [ ] `alembic downgrade -1` succeeds and removes the table (verify round-trip)

## Repository

- [ ] `EmbeddingRepository.upsert()` implemented
- [ ] `EmbeddingRepository.get_all_vectors()` implemented

## Embedding client

- [ ] `backend/src/llm/embedding.py` — `EmbeddingClient.embed()` implemented
- [ ] Uses `settings.EMBEDDING_MODEL` as default model

## Deduplication service

- [ ] `backend/src/dedup/service.py` — `DeduplicationService.is_duplicate()` implemented
- [ ] Pure-Python cosine similarity (no numpy import)
- [ ] `settings.DEDUP_THRESHOLD` used as default threshold

## Settings

- [ ] `EMBEDDING_MODEL` and `DEDUP_THRESHOLD` added to `Settings`

## Fixtures

- [ ] `tests/fixtures/llm/embed_case_01.json` exists
- [ ] `tests/fixtures/llm/embed_case_02_near_duplicate.json` exists

## Tests

- [ ] `tests/llm/test_embedding_client.py` — all pass
- [ ] `tests/dedup/test_dedup_service.py` — all pass (including orthogonal + edge cases)
- [ ] `tests/db/test_embedding_repository.py` — all pass
- [ ] `pytest -m "not integration" -q` — full unit suite green, no regressions

## Quality

- [ ] `mypy src/ alembic/env.py --strict` — clean
- [ ] `ruff check . && ruff format --check .` — clean

## APM output

- [ ] `report.md` written with all required sections including `§ Odchylky od spec.md`
- [ ] All checkboxes reflect actual state (DoD integrity rule)
