"""Unit tests for repository layer (mocked AsyncSession, no database)."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.answer_event import AnswerEvent
from src.db.models.bias_type import BiasType
from src.db.models.case import Case
from src.db.models.case_translation import CaseTranslation
from src.db.models.rating import Rating
from src.db.models.subscription import Subscription
from src.db.models.ui_string import UiString
from src.db.models.ui_string_translation import UiStringTranslation
from src.db.models.user import User
from src.db.repositories.answer_event import AnswerEventRepository
from src.db.repositories.bias_type import BiasTypeRepository
from src.db.repositories.case import CaseRepository
from src.db.repositories.case_translation import CaseTranslationRepository
from src.db.repositories.rating import RatingRepository
from src.db.repositories.subscription import SubscriptionRepository
from src.db.repositories.ui_string import UiStringRepository
from src.db.repositories.user import UserRepository


def _scalar_one_or_none(value: object | None) -> MagicMock:
    """Build a mock ``Result`` with ``scalar_one_or_none``."""
    result = MagicMock()
    result.scalar_one_or_none.return_value = value
    return result


def _scalar_one(value: object) -> MagicMock:
    """Build a mock ``Result`` with ``scalar_one``."""
    result = MagicMock()
    result.scalar_one.return_value = value
    return result


def _scalars_all(items: list[object]) -> MagicMock:
    """Build a mock ``Result`` with ``scalars().all()``."""
    result = MagicMock()
    scalars = MagicMock()
    scalars.all.return_value = items
    result.scalars.return_value = scalars
    return result


def _rows_all(rows: list[tuple[object, object | None]]) -> MagicMock:
    """Build a mock ``Result`` with ``all()`` returning join pairs."""
    result = MagicMock()
    result.all.return_value = rows
    return result


# --- BiasTypeRepository ---


@pytest.mark.unit
async def test_bias_type_repository_get_by_slug_found() -> None:
    """Return row when slug exists."""
    bt = BiasType(slug="anchoring", name_en="A", description_en="D")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(bt))
    repo = BiasTypeRepository(mock_session)
    result = await repo.get_by_slug("anchoring")
    assert result is bt
    mock_session.execute.assert_awaited_once()


@pytest.mark.unit
async def test_bias_type_repository_get_by_slug_not_found() -> None:
    """Return None when slug missing."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = BiasTypeRepository(mock_session)
    assert await repo.get_by_slug("nope") is None


@pytest.mark.unit
async def test_bias_type_repository_get_by_id_found() -> None:
    """``get_by_id`` delegates to ``session.get``."""
    bt = BiasType(slug="s", name_en="n", description_en="d")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=bt)
    repo = BiasTypeRepository(mock_session)
    assert await repo.get_by_id(1) is bt
    mock_session.get.assert_awaited_once_with(BiasType, 1)


@pytest.mark.unit
async def test_bias_type_repository_get_by_id_not_found() -> None:
    """``get_by_id`` returns None when key missing."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=None)
    repo = BiasTypeRepository(mock_session)
    assert await repo.get_by_id(99) is None


@pytest.mark.unit
async def test_bias_type_repository_list_empty() -> None:
    """``list`` yields empty when scalars return no rows."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = BiasTypeRepository(mock_session)
    assert await repo.list() == []


@pytest.mark.unit
async def test_bias_type_repository_list_nonempty() -> None:
    """``list`` returns scalar rows."""
    bt = BiasType(slug="s", name_en="n", description_en="d")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([bt]))
    repo = BiasTypeRepository(mock_session)
    assert await repo.list(limit=5, offset=0) == [bt]


@pytest.mark.unit
async def test_bias_type_repository_add_flushes() -> None:
    """``add`` calls ``add`` + ``flush`` without commit."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = BiasTypeRepository(mock_session)
    bt = BiasType(slug="s", name_en="n", description_en="d")
    out = await repo.add(bt)
    mock_session.add.assert_called_once_with(bt)
    mock_session.flush.assert_awaited_once()
    assert out is bt


@pytest.mark.unit
async def test_bias_type_repository_delete_flushes() -> None:
    """``delete`` awaits ``delete`` + ``flush``."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = BiasTypeRepository(mock_session)
    bt = BiasType(slug="s", name_en="n", description_en="d")
    await repo.delete(bt)
    mock_session.delete.assert_awaited_once_with(bt)
    mock_session.flush.assert_awaited_once()


# --- CaseRepository ---


@pytest.mark.unit
async def test_case_repository_get_by_bias_type_found() -> None:
    """Return cases for bias type and status filter."""
    cid = uuid.uuid4()
    case = Case(bias_type_id=1, id=cid, parametric_payload={})
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([case]))
    repo = CaseRepository(mock_session)
    rows = await repo.get_by_bias_type(1, status="active")
    assert rows == [case]


@pytest.mark.unit
async def test_case_repository_get_by_bias_type_empty() -> None:
    """Return empty list when no cases match."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = CaseRepository(mock_session)
    assert await repo.get_by_bias_type(2) == []


@pytest.mark.unit
async def test_case_repository_update_rating_executes_update() -> None:
    """``update_rating`` issues one UPDATE statement."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = CaseRepository(mock_session)
    case_id = uuid.uuid4()
    await repo.update_rating(case_id, stars=4)
    mock_session.execute.assert_awaited_once()


@pytest.mark.unit
async def test_case_repository_get_by_id_uuid() -> None:
    """Load case by UUID primary key."""
    case_id = uuid.uuid4()
    case = Case(bias_type_id=1, id=case_id, parametric_payload={})
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=case)
    repo = CaseRepository(mock_session)
    assert await repo.get_by_id(case_id) is case


@pytest.mark.unit
async def test_case_repository_list_empty() -> None:
    """``list`` can be empty for cases."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = CaseRepository(mock_session)
    assert await repo.list(offset=0) == []


@pytest.mark.unit
async def test_case_repository_add_and_delete() -> None:
    """CRUD hooks delegate to session."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = CaseRepository(mock_session)
    case_id = uuid.uuid4()
    case = Case(bias_type_id=1, id=case_id, parametric_payload={})
    assert await repo.add(case) is case
    await repo.delete(case)
    mock_session.delete.assert_awaited_once_with(case)


# --- CaseTranslationRepository ---


@pytest.mark.unit
async def test_case_translation_get_by_case_and_locale_found() -> None:
    """Return translation row."""
    case_id = uuid.uuid4()
    tr = CaseTranslation(
        case_id=case_id,
        locale="cs",
        title="t",
        question="q",
        options=[],
        correct_option=0,
        explanation="e",
        source_hash="h",
    )
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(tr))
    repo = CaseTranslationRepository(mock_session)
    assert await repo.get_by_case_and_locale(case_id, "cs") is tr


@pytest.mark.unit
async def test_case_translation_get_by_case_and_locale_none() -> None:
    """Return None when pair missing."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = CaseTranslationRepository(mock_session)
    case_id = uuid.uuid4()
    assert await repo.get_by_case_and_locale(case_id, "en") is None


@pytest.mark.unit
async def test_case_translation_get_by_id_uuid_pk() -> None:
    """Case translation uses UUID PK."""
    tid = uuid.uuid4()
    case_id = uuid.uuid4()
    tr = CaseTranslation(
        id=tid,
        case_id=case_id,
        locale="en",
        title="t",
        question="q",
        options=[],
        correct_option=0,
        explanation="e",
        source_hash="h",
    )
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=tr)
    repo = CaseTranslationRepository(mock_session)
    assert await repo.get_by_id(tid) is tr


@pytest.mark.unit
async def test_case_translation_list_add_delete() -> None:
    """Base methods flush correctly."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = CaseTranslationRepository(mock_session)
    case_id = uuid.uuid4()
    tr = CaseTranslation(
        case_id=case_id,
        locale="en",
        title="t",
        question="q",
        options=[],
        correct_option=0,
        explanation="e",
        source_hash="h",
    )
    await repo.add(tr)
    await repo.delete(tr)


# --- UiStringRepository ---


@pytest.mark.unit
async def test_ui_string_get_all_keys_nonempty() -> None:
    """Return ordered ui strings."""
    u = UiString(key="k", title="t", description="d", source_hash="h")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([u]))
    repo = UiStringRepository(mock_session)
    assert await repo.get_all_keys() == [u]


@pytest.mark.unit
async def test_ui_string_get_all_keys_empty() -> None:
    """Empty catalog."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = UiStringRepository(mock_session)
    assert await repo.get_all_keys() == []


@pytest.mark.unit
async def test_ui_string_get_translation_found() -> None:
    """Fetch one translation."""
    tr = UiStringTranslation(key="k", locale="cs", title_translated="T", source_hash="h")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(tr))
    repo = UiStringRepository(mock_session)
    assert await repo.get_translation("k", "cs") is tr


@pytest.mark.unit
async def test_ui_string_get_translation_none() -> None:
    """Missing translation returns None."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = UiStringRepository(mock_session)
    assert await repo.get_translation("k", "xx") is None


@pytest.mark.unit
async def test_ui_string_get_all_with_translation_pairs() -> None:
    """Left join yields (UiString, translation or None) pairs."""
    u = UiString(key="k", title="t", description="d", source_hash="h")
    tr = UiStringTranslation(key="k", locale="cs", title_translated="T", source_hash="h")
    u2 = UiString(key="k2", title="t2", description="d2", source_hash="h2")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_rows_all([(u, tr), (u2, None)]))
    repo = UiStringRepository(mock_session)
    pairs = await repo.get_all_with_translation("cs")
    assert len(pairs) == 2
    assert pairs[0] == (u, tr)
    assert pairs[1][0] is u2
    assert pairs[1][1] is None


@pytest.mark.unit
async def test_ui_string_upsert_translation_returns_row() -> None:
    """``upsert_translation`` returns RETURNING row."""
    tr = UiStringTranslation(key="k", locale="cs", title_translated="T", source_hash="nh")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one(tr))
    repo = UiStringRepository(mock_session)
    out = await repo.upsert_translation("k", "cs", "T", None, "nh")
    assert out is tr
    mock_session.execute.assert_awaited_once()


@pytest.mark.unit
async def test_ui_string_get_by_id_text_pk() -> None:
    """UiString primary key is text."""
    u = UiString(key="x", title="t", description="d", source_hash="h")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=u)
    repo = UiStringRepository(mock_session)
    assert await repo.get_by_id("x") is u


@pytest.mark.unit
async def test_ui_string_list_add_delete() -> None:
    """Base CRUD for UiString."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = UiStringRepository(mock_session)
    u = UiString(key="z", title="t", description="d", source_hash="h")
    await repo.add(u)
    await repo.delete(u)


# --- UserRepository ---


@pytest.mark.unit
async def test_user_get_by_email_found() -> None:
    """Lookup by email."""
    user = User(email="a@b.c", is_premium=False)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(user))
    repo = UserRepository(mock_session)
    assert await repo.get_by_email("a@b.c") is user


@pytest.mark.unit
async def test_user_get_by_email_none() -> None:
    """Unknown email."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = UserRepository(mock_session)
    assert await repo.get_by_email("none@x.y") is None


@pytest.mark.unit
async def test_user_get_by_id_and_list() -> None:
    """UUID PK path."""
    user = User(email=None, is_premium=False)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=user)
    mock_session.execute = AsyncMock(return_value=_scalars_all([user]))
    repo = UserRepository(mock_session)
    uid = user.id
    assert await repo.get_by_id(uid) is user
    assert await repo.list() == [user]


# --- AnswerEventRepository ---


@pytest.mark.unit
async def test_answer_event_list_by_user_nonempty() -> None:
    """Return events for user."""
    uid = uuid.uuid4()
    case_id = uuid.uuid4()
    ev = AnswerEvent(user_id=uid, case_id=case_id, chosen_option=1, is_correct=True)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([ev]))
    repo = AnswerEventRepository(mock_session)
    assert await repo.list_by_user(uid) == [ev]


@pytest.mark.unit
async def test_answer_event_list_by_user_empty() -> None:
    """No events."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = AnswerEventRepository(mock_session)
    assert await repo.list_by_user(uuid.uuid4()) == []


@pytest.mark.unit
async def test_answer_event_crud_base() -> None:
    """Flush semantics for answer events."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = AnswerEventRepository(mock_session)
    case_id = uuid.uuid4()
    ev = AnswerEvent(user_id=None, case_id=case_id, chosen_option=0, is_correct=False)
    await repo.add(ev)
    await repo.delete(ev)


@pytest.mark.unit
async def test_answer_event_get_by_id_none() -> None:
    """``get_by_id`` empty."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=None)
    repo = AnswerEventRepository(mock_session)
    assert await repo.get_by_id(uuid.uuid4()) is None


# --- RatingRepository ---


@pytest.mark.unit
async def test_rating_get_by_user_and_case_found() -> None:
    """Return rating tuple."""
    uid = uuid.uuid4()
    case_id = uuid.uuid4()
    r = Rating(user_id=uid, case_id=case_id, stars=5)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(r))
    repo = RatingRepository(mock_session)
    assert await repo.get_by_user_and_case(uid, case_id) is r


@pytest.mark.unit
async def test_rating_get_by_user_and_case_none() -> None:
    """No rating yet."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = RatingRepository(mock_session)
    assert await repo.get_by_user_and_case(uuid.uuid4(), uuid.uuid4()) is None


@pytest.mark.unit
async def test_rating_list_empty() -> None:
    """List ratings via base."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([]))
    repo = RatingRepository(mock_session)
    assert await repo.list() == []


@pytest.mark.unit
async def test_rating_get_by_id_found() -> None:
    """Load rating by UUID."""
    uid = uuid.uuid4()
    case_id = uuid.uuid4()
    rid = uuid.uuid4()
    r = Rating(id=rid, user_id=uid, case_id=case_id, stars=3)
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get = AsyncMock(return_value=r)
    repo = RatingRepository(mock_session)
    assert await repo.get_by_id(rid) is r


# --- SubscriptionRepository ---


@pytest.mark.unit
async def test_subscription_get_active_by_user_found() -> None:
    """Return active sub."""
    uid = uuid.uuid4()
    sub = Subscription(user_id=uid, status="active")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(sub))
    repo = SubscriptionRepository(mock_session)
    assert await repo.get_active_by_user(uid) is sub


@pytest.mark.unit
async def test_subscription_get_active_by_user_none() -> None:
    """No active subscription."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalar_one_or_none(None))
    repo = SubscriptionRepository(mock_session)
    assert await repo.get_active_by_user(uuid.uuid4()) is None


@pytest.mark.unit
async def test_subscription_add_delete() -> None:
    """Base methods."""
    mock_session = AsyncMock(spec=AsyncSession)
    repo = SubscriptionRepository(mock_session)
    sub = Subscription(user_id=uuid.uuid4(), status="inactive")
    await repo.add(sub)
    await repo.delete(sub)


@pytest.mark.unit
async def test_subscription_list_nonempty() -> None:
    """Base list returns rows."""
    sub = Subscription(user_id=uuid.uuid4(), status="inactive")
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=_scalars_all([sub]))
    repo = SubscriptionRepository(mock_session)
    assert await repo.list() == [sub]
