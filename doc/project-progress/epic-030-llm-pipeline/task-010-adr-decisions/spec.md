---
apm_category: task-spec
apm_ref: E030.T010
apm_level: task
created_by: Planner
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E030.T010 — ADR-003 + ADR-004: Architecture Decision Records

## Goal

Commit the two Architecture Decision Records documenting the LLM and embedding provider
choices approved in the E030 epic plan. Also declare the `openai` SDK as a project
dependency and document `OPENAI_API_KEY` in `.env.example`.

## Context Bundle

### Files to read (do NOT modify)
- `doc/project-progress/epic-030-llm-pipeline/plan.md` — full provider rationale
- `doc/architecture/decisions/ADR-001-use-postgresql.md` — ADR format reference
- `doc/architecture/decisions/ADR-002-ethics-framework.md` — second format reference
- `backend/pyproject.toml` — dependency format

### Files to create / modify
- **Create**: `doc/architecture/decisions/ADR-003-llm-provider.md`
- **Create**: `doc/architecture/decisions/ADR-004-embedding-model.md`
- **Modify**: `backend/pyproject.toml` — add `openai>=1.30.0` to base `[project.dependencies]`
- **Modify**: `.env.example` — add `OPENAI_API_KEY=` with a comment explaining it is required
  for LLM and embedding calls; leave the value empty (never commit a real key)

### APM Output
Coder MUST write `doc/project-progress/epic-030-llm-pipeline/task-010-adr-decisions/report.md`
and fill `task-010-adr-decisions/dod.md` at task end.

## ADR-003 Content (LLM Provider)

Use the standard ADR template:

```markdown
# ADR-003: Use OpenAI GPT-4o-mini as the LLM Provider

**Status**: Accepted
**Date**: 2026-05-10
**Epic**: E030

## Context
The MVP requires an LLM for Case generation and LLM-as-judge validation.
Candidates evaluated: OpenAI GPT-4o-mini, Anthropic Claude 3.5 Haiku, Google Gemini 2.0 Flash.

## Decision
Use OpenAI GPT-4o-mini via the `openai` Python SDK (≥ 1.30.0).

## Rationale
- Best cost / quality trade-off: $0.15/1M input, $0.60/1M output tokens.
- Estimated cost per Case (generation + judge, ~1 500 tokens): ≈ $0.001.
- At 10 000 Cases/month: ≈ $10 — within solo-developer budget.
- Excellent `response_format={"type":"json_object"}` support for structured output.
- Mature, typed Python SDK; widely documented patterns for JSON generation.
- Multi-LLM abstraction is explicitly out of MVP scope (spec.md Non-Goals).

## Consequences
+ Predictable cost at MVP scale; JSON output format reliable.
+ Single SDK dependency (openai ≥ 1.30.0).
- Lock-in to one provider for MVP; abstraction layer is a post-MVP concern.
- Requires OPENAI_API_KEY in environment; must never be committed to git.
```

## ADR-004 Content (Embedding Model)

```markdown
# ADR-004: Use OpenAI text-embedding-3-small for Deduplication

**Status**: Accepted
**Date**: 2026-05-10
**Epic**: E030

## Context
Embedding-based deduplication requires generating vector representations of Cases to
detect near-duplicate content before inserting into the cyclic buffer.

## Decision
Use OpenAI `text-embedding-3-small` (1 536 dimensions) via the same `openai` SDK.
Store vectors as PostgreSQL `FLOAT8[]` column; compute cosine similarity in Python.

## Rationale
- Piggybacks on the existing OpenAI dependency from ADR-003 — no new infrastructure.
- Cost: $0.02/1M tokens. For 25 seed Cases + buffer of ~200 Cases: < $0.01 total.
- No additional Docker services, no torch, no sentence-transformers (+400 MB image).
- `FLOAT8[]` in PostgreSQL is sufficient for < 1 000 Cases at MVP scale.
- pgvector migration is straightforward if post-MVP scale requires ANN search.

## Consequences
+ Zero additional infrastructure for MVP.
+ Negligible marginal cost per Case.
- Requires same OPENAI_API_KEY as ADR-003.
- Python-side cosine similarity is O(n) scan; acceptable for < 1 000 Cases.
- If buffer exceeds ~10 000 Cases, migrate to pgvector for ANN search (post-MVP).
```

## Test Specification

No automated tests for this task (documentation-only). Verify:
- `pip install -e "./backend[dev]"` still succeeds with the added `openai` dependency.
- Both ADR files are valid Markdown (render without errors).

## APM Output

See `dod.md` in this directory.
