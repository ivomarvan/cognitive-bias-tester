---
apm_category: task-spec
apm_ref: E020.T030
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T030 — Seed Data

## Goal

Author JSON fixture data for 5 bias types, 25 gold-standard English Cases (5 per bias type),
and the initial set of UI string keys. Implement an idempotent async seed script that inserts
all fixtures via the repository layer.

## Depends on

T010 (models), T020 (repositories).

## Inputs

- `backend/src/db/models/` — all models
- `backend/src/db/repositories/` — all repositories
- `backend/src/db/session.py` — `async_session`
- `frontend/src/locales/en.json` — existing UI keys to migrate into UiString format (read only)
- `doc/project-progress/spec.md` — 5 MVP bias types, parametric placeholder list
- `doc/project-progress/epic-020-data-model/plan.md` — fixture JSON formats (§ T030)

## Outputs

- `backend/src/db/seed/__init__.py`
- `backend/src/db/seed/bias_types.json`
- `backend/src/db/seed/cases.json` (25 entries)
- `backend/src/db/seed/ui_strings.json`
- `backend/src/db/seed/seed.py`
- `backend/tests/db/test_seed.py`

## Implementation Notes

### Bias types (author exactly these 5)

```json
[
  {"slug": "anchoring",          "name_en": "Anchoring Bias",       "description_en": "The tendency to rely too heavily on the first piece of information encountered when making decisions."},
  {"slug": "framing",            "name_en": "Framing Effect",       "description_en": "The tendency to react differently to the same information depending on how it is presented."},
  {"slug": "loss_aversion",      "name_en": "Loss Aversion",        "description_en": "The tendency to prefer avoiding losses over acquiring equivalent gains."},
  {"slug": "confirmation_bias",  "name_en": "Confirmation Bias",    "description_en": "The tendency to search for, interpret, and recall information that confirms one's prior beliefs."},
  {"slug": "sunk_cost",          "name_en": "Sunk Cost Fallacy",    "description_en": "The tendency to continue a behaviour due to past investments, even when stopping is the better choice."}
]
```

### Cases (25 total — author all content)

Write **5 Cases per bias type** — each must be:
- A realistic, concrete scenario (person/organisation facing a decision), 3–5 sentences
- Framed so one of the 4 options is clearly the unbiased rational choice (the `correct_option`)
- Using parametric placeholders where natural: `{local_first_name}`, `{currency_amount_small}`,
  `{currency_amount_large}`, `{timeframe_days}`, `{percentage}`
- Varied in domain (finance, health, work, consumer, social)
- Self-contained — reader needs no external knowledge

**JSON format per Case:**
```json
{
  "bias_type_slug": "anchoring",
  "variant": 0,
  "parametric_payload": {
    "local_first_name": "Alex",
    "currency_amount_small": 20,
    "currency_amount_large": 500
  },
  "locale": "en",
  "title": "The Car Negotiation",
  "question": "{local_first_name} is buying a used car. The seller opens with {currency_amount_large} €. {local_first_name} immediately thinks that {currency_amount_small} € below the asking price would be a fair deal. What should {local_first_name} do instead?",
  "options": [
    {"label": "A", "text": "Offer {currency_amount_small} € below the asking price"},
    {"label": "B", "text": "Research the market value independently, then make an offer based on that"},
    {"label": "C", "text": "Accept the asking price — the seller must know what it's worth"},
    {"label": "D", "text": "Walk away without making any offer"}
  ],
  "correct_option": 1,
  "explanation": "The opening price acts as an anchor, pulling {local_first_name}'s reference point toward the seller's number. The rational approach is to gather independent market data and base the offer on that, not on the seller's opening bid."
}
```

`correct_option` is the 0-based index (0 = A, 1 = B, 2 = C, 3 = D).

### UiString keys (ui_strings.json)

Migrate all keys from `frontend/src/locales/en.json` into the structured format below.
Add any additional keys needed for MVP UI chrome (at minimum cover: app title, home page
heading, navigation items, answer button, result captions, error messages, settings labels,
footer text, bias type display names). Aim for completeness — missing keys in production will
fall back to English, but explicit coverage is preferred.

```json
{
  "app_title": {
    "title": "Cognitive Bias Tester",
    "description": "The application name shown in the browser tab title and main page header."
  },
  "home_heading": {
    "title": "Train your brain to think clearly.",
    "description": "Hero headline on the anonymous landing / home page."
  },
  "nav_settings": {
    "title": "Settings",
    "description": "Navigation menu item leading to the user settings page."
  }
}
```

`source_hash` is computed by `seed.py` at insert time — do NOT hardcode it in the JSON file.

### seed.py

```python
"""Idempotent database seed script.

Usage: python -m src.db.seed.seed

Inserts all fixture data via repositories. Uses INSERT ON CONFLICT DO NOTHING
(idempotent). Logs inserted vs skipped counts per entity type to INFO.
"""
import asyncio
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

async def seed() -> None:
    # 1. Load JSON fixtures
    # 2. Open async_session
    # 3. For each bias_type: repo.add() wrapped in try/except IntegrityError (skip on conflict)
    # 4. For each case: insert Case + CaseTranslation(locale="en")
    # 5. For each ui_string: compute source_hash, repo.add()
    # 6. commit session
    # 7. log counts

if __name__ == "__main__":
    asyncio.run(seed())
```

For idempotency, catch `sqlalchemy.exc.IntegrityError` on each insert and skip (log as DEBUG).
Alternatively, use `session.merge()` for bias types (PK is slug-derived int, merge by slug lookup).

### source_hash for UiString
```python
import hashlib

def compute_source_hash(key: str, title: str, description: str) -> str:
    return hashlib.sha256(
        f"{key}|{title}|{description}".encode("utf-8")
    ).hexdigest()
```

## Test Specification

File: `backend/tests/db/test_seed.py`, marker `unit`

```python
@pytest.mark.unit
async def test_seed_inserts_bias_types_on_first_run() -> None:
    # Mock repositories; assert add() called 5 times for bias_type

@pytest.mark.unit
async def test_seed_skips_existing_bias_types() -> None:
    # Mock repo.get_by_slug to return existing BiasType; assert add() NOT called

@pytest.mark.unit
async def test_seed_inserts_25_cases() -> None:
    # Assert CaseRepository.add() called exactly 25 times

@pytest.mark.unit
async def test_seed_computes_source_hash_for_ui_strings() -> None:
    # Assert UiStringRepository.add() called with non-empty source_hash
```

## Regression Check

```bash
ruff check .
ruff format --check .
mypy src/ --strict
pytest -m "not integration" -q
```

All must exit 0.

## Definition of Done

See [dod.md](dod.md).
