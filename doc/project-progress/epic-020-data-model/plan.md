---
apm_category: epic-plan
apm_ref: E020
apm_level: epic
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder, Human
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Epic Plan: E020 — Data Model & Seed Cases

## Epic Goal

Establish the complete domain model for the MVP: nine SQLAlchemy ORM entities covering Cases,
translations, users, ratings, UI strings, and subscriptions; a repository layer for all entities;
seeded fixture data (5 bias types, 25 gold-standard Cases, initial UI string keys); a backend
`GET /v1/i18n/{locale}` endpoint with hash-based lookup and English fallback; and a typed
`CyclicBuffer` protocol stub to unblock E030. No business logic is implemented in this Epic —
only the data layer and interfaces.

---

## Task List

| Task | Name | Depends on | Coder model |
|------|------|-----------|-------------|
| T010 | Domain Models + Alembic Migration | — | Composer-2 |
| T020 | Repository Layer | T010 | Composer-2 |
| T030 | Seed Data | T010, T020 | Composer-2 |
| T040 | i18n API Endpoint | T010, T020 | Composer-2 |
| T050 | Cyclic Buffer Stub | — | Composer-2 |

T010 and T050 can start in parallel.
T030 and T040 can start in parallel once T010 + T020 are done.

---

## Cross-Task Conventions

- All new Python files in `backend/src/` must pass `ruff check`, `ruff format --check`, and `mypy src/ --strict` with exit 0.
- All new tests go in `backend/tests/` mirroring `backend/src/` structure. Marker `unit` for tests with no DB; `integration` for tests needing live PostgreSQL.
- Alembic migrations live in `backend/alembic/versions/`. Use `alembic revision --autogenerate` only with all models imported; verify with `alembic check` after generation.
- JSON fixture files in `backend/src/db/seed/` are UTF-8, 2-space indented, committed to git.
- The `sha256`-based `source_hash` is computed as `sha256(f"{key}|{title}|{description}".encode("utf-8")).hexdigest()`.
- No changes to `frontend/` in this Epic — i18n API wiring to Vue is in E040.
- Branch: `feature/E020-data-model`.

---

## Task Specifications

### T010 — Domain Models + Alembic Migration

**Goal:** Define all SQLAlchemy 2.x ORM models for the MVP domain and generate Alembic migration `0002_domain_model`.

**Inputs:**
- `backend/src/db/base.py` (DeclarativeBase already exists from T040/E010)
- `backend/src/db/models/__init__.py` (currently empty)
- `backend/alembic/versions/0001_initial.py` (empty baseline migration)
- `doc/project-progress/spec.md` — domain entity list and i18n strategy
- `doc/project-progress/epic-020-data-model/plan.md` — model field specs below

**Outputs:**
- `backend/src/db/models/bias_type.py`
- `backend/src/db/models/case.py`
- `backend/src/db/models/case_translation.py`
- `backend/src/db/models/ui_string.py`
- `backend/src/db/models/ui_string_translation.py`
- `backend/src/db/models/user.py`
- `backend/src/db/models/answer_event.py`
- `backend/src/db/models/rating.py`
- `backend/src/db/models/subscription.py`
- Updated `backend/src/db/models/__init__.py` — imports all models (so Alembic autogenerate detects them)
- `backend/alembic/versions/0002_domain_model.py` — generated migration
- `backend/tests/db/test_models.py` — unit tests

**Model field specifications:**

```python
# bias_type.py — table: bias_type
class BiasType(Base):
    __tablename__ = "bias_type"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)   # e.g. "anchoring"
    name_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

# case.py — table: "case" (quoted — reserved word)
class Case(Base):
    __tablename__ = "case"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bias_type_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey("bias_type.id"), nullable=False)
    source: Mapped[str] = mapped_column(Text, nullable=False, default="seed")  # "seed" | "generated"
    status: Mapped[str] = mapped_column(Text, nullable=False, default="active") # "active" | "evicted" | "draft"
    variant: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)  # 0=A, 1=B
    parametric_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # embedding column added in E030 (pgvector); omit here
    rating_sum: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rating_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

# case_translation.py — table: case_translation
class CaseTranslation(Base):
    __tablename__ = "case_translation"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("case.id", ondelete="CASCADE"), nullable=False)
    locale: Mapped[str] = mapped_column(Text, nullable=False)              # "en", "cs", "ru", …
    title: Mapped[str] = mapped_column(Text, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSONB, nullable=False)           # [{"label":"A","text":"…"}, …]
    correct_option: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0-3 index
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    source_hash: Mapped[str] = mapped_column(Text, nullable=False)         # sha256 of English source
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("case_id", "locale"),)

# ui_string.py — table: ui_string
class UiString(Base):
    __tablename__ = "ui_string"
    key: Mapped[str] = mapped_column(Text, primary_key=True)               # e.g. "settings_main_menu"
    title: Mapped[str] = mapped_column(Text, nullable=False)               # English display text
    description: Mapped[str] = mapped_column(Text, nullable=False)         # context hint for translators
    source_hash: Mapped[str] = mapped_column(Text, nullable=False)         # sha256(key|title|description)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

# ui_string_translation.py — table: ui_string_translation
class UiStringTranslation(Base):
    __tablename__ = "ui_string_translation"
    key: Mapped[str] = mapped_column(Text, ForeignKey("ui_string.key", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    locale: Mapped[str] = mapped_column(Text, primary_key=True)
    source_hash: Mapped[str] = mapped_column(Text, nullable=False)         # hash of ui_string when translated
    title_translated: Mapped[str] = mapped_column(Text, nullable=False)
    description_translated: Mapped[str | None] = mapped_column(Text)      # optional, for editor tools
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

# user.py — table: "user" (quoted)
class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str | None] = mapped_column(Text, unique=True)           # null = anonymous
    is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    preferred_locale: Mapped[str | None] = mapped_column(Text)             # user-selected language
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

# answer_event.py — table: answer_event
class AnswerEvent(Base):
    __tablename__ = "answer_event"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"))
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("case.id"), nullable=False)
    chosen_option: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 0-3
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

# rating.py — table: rating
class Rating(Base):
    __tablename__ = "rating"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"))
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("case.id"), nullable=False)
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("user_id", "case_id"),
        CheckConstraint("stars BETWEEN 1 AND 5", name="ck_rating_stars"),
    )

# subscription.py — table: subscription
class Subscription(Base):
    __tablename__ = "subscription"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    stripe_sub_id: Mapped[str | None] = mapped_column(Text, unique=True)   # null until E060
    status: Mapped[str] = mapped_column(Text, nullable=False, default="inactive")  # "active"|"cancelled"|"inactive"
    started_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
```

**Alembic workflow:**
1. Import all models in `backend/src/db/models/__init__.py`
2. `alembic revision --autogenerate -m "domain_model"` inside `backend/` container
3. Review generated file; ensure `schema="public"` is not hardcoded
4. `alembic upgrade head` — verify exit 0 with live DB
5. `alembic check` — verify no pending changes

**Test specification:**
- `test_models.py` — instantiate each model with minimal required fields; assert attributes exist; no DB needed (pure unit test, marker `unit`)
- Do NOT write integration tests that test FK constraints at DB level — that is covered by the migration itself

**Context Bundle:**
- Read: `backend/src/db/base.py`, `backend/src/db/session.py`, `backend/alembic/env.py`
- Read: `doc/project-progress/spec.md` (Data Model section, UI translation section)
- Read: `doc/project-progress/epic-020-data-model/plan.md` (this file — model fields above)
- Do NOT modify: `docker-compose.yml`, `backend/src/main.py`, `backend/src/api/`
- Files NOT to modify: `doc/**`

**Recommended Coder model:** Composer-2

---

### T020 — Repository Layer

**Goal:** Implement a typed generic `Repository[T]` base class and concrete repositories for all domain entities.

**Inputs:**
- All model files from T010
- `backend/src/db/session.py` (AsyncSession, async_session)
- `backend/src/db/base.py`

**Outputs:**
- `backend/src/db/repositories/__init__.py`
- `backend/src/db/repositories/base.py` — abstract generic base
- `backend/src/db/repositories/bias_type.py`
- `backend/src/db/repositories/case.py`
- `backend/src/db/repositories/case_translation.py`
- `backend/src/db/repositories/ui_string.py`
- `backend/src/db/repositories/user.py`
- `backend/src/db/repositories/answer_event.py`
- `backend/src/db/repositories/rating.py`
- `backend/src/db/repositories/subscription.py`
- `backend/tests/db/test_repositories.py`

**Repository interface specification:**

```python
# base.py — Pattern: Repository (GoF Data Access Object variant)
from typing import Generic, TypeVar
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")

class Repository(Generic[ModelT]):
    def __init__(self, session: AsyncSession) -> None: ...
    async def get_by_id(self, id: UUID | int | str) -> ModelT | None: ...
    async def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]: ...
    async def add(self, instance: ModelT) -> ModelT: ...
    async def delete(self, instance: ModelT) -> None: ...

# bias_type.py
class BiasTypeRepository(Repository[BiasType]):
    async def get_by_slug(self, slug: str) -> BiasType | None: ...

# case.py
class CaseRepository(Repository[Case]):
    async def get_by_bias_type(self, bias_type_id: int, status: str = "active") -> list[Case]: ...
    async def update_rating(self, case_id: UUID, stars: int) -> None:
        # increment rating_sum += stars, rating_count += 1 atomically

# case_translation.py
class CaseTranslationRepository(Repository[CaseTranslation]):
    async def get_by_case_and_locale(self, case_id: UUID, locale: str) -> CaseTranslation | None: ...

# ui_string.py — most complex, used by T040
class UiStringRepository(Repository[UiString]):
    async def get_all_keys(self) -> list[UiString]: ...
    async def get_translation(self, key: str, locale: str) -> UiStringTranslation | None: ...
    async def get_all_with_translation(self, locale: str) -> list[tuple[UiString, UiStringTranslation | None]]:
        # Returns all UiString rows LEFT OUTER JOINed with UiStringTranslation for given locale
    async def upsert_translation(
        self, key: str, locale: str, title_translated: str,
        description_translated: str | None, source_hash: str
    ) -> UiStringTranslation: ...

# user.py
class UserRepository(Repository[User]):
    async def get_by_email(self, email: str) -> User | None: ...

# answer_event.py
class AnswerEventRepository(Repository[AnswerEvent]):
    async def list_by_user(self, user_id: UUID, limit: int = 100) -> list[AnswerEvent]: ...

# rating.py
class RatingRepository(Repository[Rating]):
    async def get_by_user_and_case(self, user_id: UUID, case_id: UUID) -> Rating | None: ...

# subscription.py
class SubscriptionRepository(Repository[Subscription]):
    async def get_active_by_user(self, user_id: UUID) -> Subscription | None: ...
```

**Test specification:**
- Use `AsyncMock` and `MagicMock` to mock `AsyncSession` — no live DB needed
- Test each repository method: happy path (returns expected value) + empty/None path
- Marker: `unit`

**Context Bundle:**
- Read: T010 outputs (all model files in `backend/src/db/models/`)
- Read: `backend/src/db/session.py`
- Read: `doc/project-progress/epic-020-data-model/plan.md` (repository specs above)
- Do NOT modify: `backend/src/api/`, `backend/src/main.py`, `docker-compose.yml`
- Files NOT to modify: `doc/**`

**Recommended Coder model:** Composer-2

---

### T030 — Seed Data

**Goal:** Author fixture data for 5 bias types, 25 gold-standard Cases, and initial UI string keys; implement an idempotent seed script.

**Inputs:**
- T010 models, T020 repositories
- `frontend/src/locales/en.json` — existing UI keys to migrate into UiString format
- `doc/project-progress/spec.md` — parametric placeholder list, 5 MVP bias types

**Outputs:**
- `backend/src/db/seed/__init__.py`
- `backend/src/db/seed/bias_types.json`
- `backend/src/db/seed/cases.json`
- `backend/src/db/seed/ui_strings.json`
- `backend/src/db/seed/seed.py` — async CLI entry point
- `backend/tests/db/test_seed.py`

**Bias types (5):**

| slug | name_en |
|------|---------|
| `anchoring` | Anchoring Bias |
| `framing` | Framing Effect |
| `loss_aversion` | Loss Aversion |
| `confirmation_bias` | Confirmation Bias |
| `sunk_cost` | Sunk Cost Fallacy |

**Case fixture format** (`cases.json`):
```json
[
  {
    "bias_type_slug": "anchoring",
    "variant": 0,
    "parametric_payload": {
      "currency_amount_small": 10,
      "currency_amount_large": 500,
      "local_first_name": "Alex"
    },
    "locale": "en",
    "title": "The Negotiation",
    "question": "Alex is buying a used car. The seller opens with {currency_amount_large} €. …",
    "options": [
      {"label": "A", "text": "Offer {currency_amount_small} € below the asking price"},
      {"label": "B", "text": "Research market value first, then make an independent offer"},
      {"label": "C", "text": "Accept the asking price as fair"},
      {"label": "D", "text": "Walk away immediately"}
    ],
    "correct_option": 1,
    "explanation": "The opening price acts as an anchor …"
  },
  …
]
```

Author **25 Cases** — 5 per bias type, realistic short scenarios (3–5 sentences), using parametric placeholders `{local_first_name}`, `{currency_amount_small}`, `{currency_amount_large}`, `{timeframe_days}`, `{percentage}` where appropriate. Each Case must have exactly 4 options with one correct.

**UiString fixture format** (`ui_strings.json`):
```json
{
  "app_title": {
    "title": "Cognitive Bias Tester",
    "description": "The application name shown in the browser tab and main header."
  },
  "home_heading": {
    "title": "Train your brain to think clearly.",
    "description": "Hero headline on the home page."
  },
  "nav_settings": {
    "title": "Settings",
    "description": "Navigation menu item leading to the user settings page."
  }
}
```

Migrate all keys from `frontend/src/locales/en.json` into this format, adding a descriptive `description` for each key. Add any additional keys needed for the MVP UI chrome (at minimum: app title, home heading, nav items, answer button labels, result captions, error messages, footer).

**seed.py CLI:**
```python
# python -m src.db.seed.seed  →  idempotent: INSERT OR IGNORE (ON CONFLICT DO NOTHING)
# Logs inserted vs skipped counts per entity type
# source_hash computed at seed time for each UiString
```

**Test specification:**
- Unit test: mock repositories; assert `seed.py` calls `add()` for each fixture row on first run
- Unit test: mock repositories returning existing rows; assert no duplicate inserts
- Marker: `unit`

**Context Bundle:**
- Read: T010 model files, T020 repository files
- Read: `frontend/src/locales/en.json`, `frontend/src/locales/cs.json` (for reference)
- Read: `doc/project-progress/spec.md` (Parametric Case structure, 5 bias types)
- Read: `doc/project-progress/epic-020-data-model/plan.md` (fixture formats above)
- Files NOT to modify: `doc/**`, `frontend/src/locales/` (read only, do not delete)

**Recommended Coder model:** Composer-2

---

### T040 — i18n API Endpoint

**Goal:** Implement `GET /v1/i18n/{locale}` — returns a JSON map of all UI chrome translations for the requested locale, with English fallback and stale-key signalling.

**Inputs:**
- T010 `UiString`, `UiStringTranslation` models
- T020 `UiStringRepository`
- `backend/src/db/session.py` (FastAPI dependency)
- `backend/src/main.py` (router registration)

**Outputs:**
- `backend/src/api/i18n.py`
- Updated `backend/src/main.py` — include i18n router
- `backend/tests/api/test_i18n.py`

**Endpoint specification:**

```
GET /v1/i18n/{locale}

Path param: locale — IETF language tag, e.g. "en", "cs", "ru", "fr"

Response 200:
{
  "locale": "cs",
  "translations": {
    "app_title": "Kognitivní Bias Tester",
    "home_heading": "Trénuj svůj mozek k jasnějšímu myšlení.",
    "nav_settings": "Nastavení",
    ...
  },
  "stale_keys": ["nav_settings"]   // keys where source_hash changed since translation
}
```

**Resolution logic per key:**
1. Load all `UiString` rows (English source)
2. LEFT JOIN `UiStringTranslation` for the requested `locale`
3. For each key:
   - No translation row → add to `translations` with English `title`; do NOT add to `stale_keys`
   - Translation row exists, `source_hash` matches → add translated `title_translated`
   - Translation row exists, `source_hash` differs → add English `title` as fallback; add key to `stale_keys`
4. Special case `locale == "en"` → always return English source directly, `stale_keys: []`

**Response model (Pydantic):**
```python
class I18nResponse(BaseModel):
    locale: str
    translations: dict[str, str]
    stale_keys: list[str]
```

**Note:** AI translation is NOT called here — `stale_keys` is a signal for E040's background job to enqueue translation. This endpoint is a read-only lookup.

**Test specification:**
- Integration test with live DB: seed 2 UiString rows; test locale=`en` → returns source titles; test locale=`fr` (no translations) → returns English fallback, `stale_keys=[]`; test locale with one fresh + one stale translation → correct categorisation. Marker: `integration`
- Unit test with mocked repository: all 3 resolution paths. Marker: `unit`

**Context Bundle:**
- Read: T010 model files (`ui_string.py`, `ui_string_translation.py`)
- Read: T020 `backend/src/db/repositories/ui_string.py`
- Read: `backend/src/api/health.py` (style reference for FastAPI router)
- Read: `backend/src/main.py`
- Read: `doc/project-progress/spec.md` (UI translation three-tier strategy)
- Read: `doc/project-progress/epic-020-data-model/plan.md` (endpoint spec above)
- Do NOT modify: `docker-compose.yml`, frontend files
- Files NOT to modify: `doc/**`

**Recommended Coder model:** Composer-2

---

### T050 — Cyclic Buffer Stub

**Goal:** Define the typed `CyclicBuffer` abstract interface and an in-memory stub implementation for unit tests. No database or persistence — full implementation is in E030.

**Inputs:**
- `backend/src/db/models/case.py` (UUID type only)
- Python 3.12 `abc` module

**Outputs:**
- `backend/src/core/cyclic_buffer.py`
- `backend/tests/core/test_cyclic_buffer.py`

**Interface specification:**

```python
# backend/src/core/cyclic_buffer.py
from abc import ABC, abstractmethod
from uuid import UUID


class CyclicBuffer(ABC):
    """Interface for the Case cyclic buffer (fully implemented in E030).

    The buffer holds a capped set of active Case IDs. Cases are inserted,
    retrieved round-robin by locale / bias type, and evicted by a composite
    (rating_avg, age) score when the buffer exceeds capacity.
    """

    @abstractmethod
    async def insert(self, case_id: UUID) -> None:
        """Add a Case ID to the buffer. No-op if already present."""

    @abstractmethod
    async def get_next(
        self,
        locale: str,
        bias_type_slug: str | None = None,
    ) -> UUID | None:
        """Return the next Case ID for the given locale, or None if empty.

        Args:
            locale: IETF language tag of the requesting user.
            bias_type_slug: Optional filter; if given, only Cases of this
                bias type are returned.

        Returns:
            A Case UUID, or None when the buffer is empty.
        """

    @abstractmethod
    async def evict_worst(self) -> int:
        """Evict Cases with the lowest composite score until buffer is at capacity.

        Returns:
            Number of Cases evicted.
        """

    @abstractmethod
    async def size(self) -> int:
        """Return the current number of Case IDs in the buffer."""


class InMemoryCyclicBuffer(CyclicBuffer):
    """Deterministic in-memory stub — for unit tests only, not production.

    Stores UUIDs in insertion order; get_next cycles round-robin;
    evict_worst removes from the end of the list.
    """

    def __init__(self, capacity: int = 100) -> None: ...
    async def insert(self, case_id: UUID) -> None: ...
    async def get_next(self, locale: str, bias_type_slug: str | None = None) -> UUID | None: ...
    async def evict_worst(self) -> int: ...
    async def size(self) -> int: ...
```

**Test specification:**
- `test_cyclic_buffer.py` — test `InMemoryCyclicBuffer`:
  - `insert` adds UUID; `size` reflects it; second `insert` of same UUID is no-op
  - `get_next` on empty buffer returns None
  - `get_next` cycles through all inserted IDs round-robin
  - `evict_worst` on buffer of 3 with capacity 2 removes 1, returns 1
- Marker: `unit`

**Context Bundle:**
- Read: `doc/project-progress/spec.md` (LLM cache cyclic buffer description)
- Read: `doc/project-progress/epic-020-data-model/plan.md` (interface spec above)
- Read: `backend/src/core/config.py`, `backend/src/core/logging.py` (style reference)
- Do NOT modify: any existing files; do NOT add DB dependencies
- Files NOT to modify: `doc/**`

**Recommended Coder model:** Composer-2
