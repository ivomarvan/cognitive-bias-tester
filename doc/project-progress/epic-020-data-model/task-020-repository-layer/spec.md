---
apm_category: task-spec
apm_ref: E020.T020
apm_level: task
created_by: Planner
model: claude-sonnet-4-6
intended_for: Coder
created_at: 2026-05-10
updated_at: 2026-05-10
---

# Task Spec: E020.T020 — Repository Layer

## Goal

Implement a typed generic `Repository[T]` base class and concrete repository classes for all
nine domain entities. No business logic — repositories are pure data access objects (Pattern:
Repository, GoF Data Access Object variant).

## Depends on

T010 (all model files must exist).

## Inputs

- `backend/src/db/models/` — all nine models from T010
- `backend/src/db/session.py` — `AsyncSession`, `async_session`, `get_session`
- `backend/src/db/base.py` — `Base`
- `doc/project-progress/epic-020-data-model/plan.md` — repository interface specs (§ T020)

## Outputs

New directory `backend/src/db/repositories/` with:

| File | Class |
|------|-------|
| `__init__.py` | exports all repository classes |
| `base.py` | `Repository[T]` generic base |
| `bias_type.py` | `BiasTypeRepository` |
| `case.py` | `CaseRepository` |
| `case_translation.py` | `CaseTranslationRepository` |
| `ui_string.py` | `UiStringRepository` |
| `user.py` | `UserRepository` |
| `answer_event.py` | `AnswerEventRepository` |
| `rating.py` | `RatingRepository` |
| `subscription.py` | `SubscriptionRepository` |

New tests:
- `backend/tests/db/test_repositories.py`

## Implementation Notes

### Base repository

```python
# Pattern: Repository (GoF Data Access Object variant)
from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")

class Repository(Generic[ModelT]):
    """Generic async repository providing standard CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, pk: ...) -> ModelT | None:
        # use session.get() for primary key lookup
        ...

    async def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        # select(ModelClass).limit(limit).offset(offset)
        ...

    async def add(self, instance: ModelT) -> ModelT:
        self._session.add(instance)
        await self._session.flush()  # assigns server-side defaults; caller commits
        return instance

    async def delete(self, instance: ModelT) -> None:
        await self._session.delete(instance)
        await self._session.flush()
```

Concrete repositories receive a `session: AsyncSession` in `__init__` and call `super().__init__(session)`.

### UiStringRepository (most complex — used by T040)

```python
class UiStringRepository(Repository[UiString]):
    async def get_all_keys(self) -> list[UiString]: ...

    async def get_translation(
        self, key: str, locale: str
    ) -> UiStringTranslation | None: ...

    async def get_all_with_translation(
        self, locale: str
    ) -> list[tuple[UiString, UiStringTranslation | None]]:
        """LEFT OUTER JOIN ui_string with ui_string_translation for given locale."""
        stmt = (
            select(UiString, UiStringTranslation)
            .outerjoin(
                UiStringTranslation,
                (UiStringTranslation.key == UiString.key)
                & (UiStringTranslation.locale == locale),
            )
        )
        result = await self._session.execute(stmt)
        return result.all()

    async def upsert_translation(
        self,
        key: str,
        locale: str,
        title_translated: str,
        description_translated: str | None,
        source_hash: str,
    ) -> UiStringTranslation:
        # Use INSERT ... ON CONFLICT (key, locale) DO UPDATE SET ...
        # via sqlalchemy dialects postgresql insert()
        ...
```

### CaseRepository

```python
class CaseRepository(Repository[Case]):
    async def get_by_bias_type(
        self, bias_type_id: int, status: str = "active"
    ) -> list[Case]: ...

    async def update_rating(self, case_id: UUID, stars: int) -> None:
        """Increment rating_sum and rating_count atomically."""
        stmt = (
            update(Case)
            .where(Case.id == case_id)
            .values(
                rating_sum=Case.rating_sum + stars,
                rating_count=Case.rating_count + 1,
                updated_at=func.now(),
            )
        )
        await self._session.execute(stmt)
```

### Dependency injection pattern
Repositories are instantiated per-request in FastAPI endpoints via `Depends`:

```python
# Example (Coder will wire this in T040):
async def get_ui_string_repo(
    session: AsyncSession = Depends(get_session),
) -> UiStringRepository:
    return UiStringRepository(session)
```

Do NOT wire endpoints in this task — only implement repositories.

## Test Specification

File: `backend/tests/db/test_repositories.py`, marker `unit`

Mock `AsyncSession` with `unittest.mock.AsyncMock`. For each repository:

```python
@pytest.mark.unit
async def test_bias_type_repository_get_by_slug_found() -> None:
    mock_session = AsyncMock(spec=AsyncSession)
    # configure mock_session.execute to return a mock result with a BiasType
    repo = BiasTypeRepository(mock_session)
    result = await repo.get_by_slug("anchoring")
    assert result is not None

@pytest.mark.unit
async def test_bias_type_repository_get_by_slug_not_found() -> None:
    mock_session = AsyncMock(spec=AsyncSession)
    # configure mock to return empty result
    repo = BiasTypeRepository(mock_session)
    result = await repo.get_by_slug("nonexistent")
    assert result is None
```

Cover at minimum: happy path + not-found/empty for every public method.

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
