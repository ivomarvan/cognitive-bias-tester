"""Unit tests for ORM models (no database)."""

from __future__ import annotations

import uuid

import pytest

from src.db.models.answer_event import AnswerEvent
from src.db.models.bias_type import BiasType
from src.db.models.case import Case
from src.db.models.case_translation import CaseTranslation
from src.db.models.rating import Rating
from src.db.models.subscription import Subscription
from src.db.models.ui_string import UiString
from src.db.models.ui_string_translation import UiStringTranslation
from src.db.models.user import User


@pytest.mark.unit
def test_bias_type_instantiation() -> None:
    """Construct ``BiasType`` with required text fields."""
    bt = BiasType(slug="anchoring", name_en="Anchoring", description_en="Desc")
    assert bt.slug == "anchoring"
    assert bt.name_en == "Anchoring"


@pytest.mark.unit
def test_user_instantiation() -> None:
    """Construct ``User`` with explicit premium flag (declarative init omits column defaults)."""
    u = User(is_premium=False)
    assert u.is_premium is False
    assert u.email is None


@pytest.mark.unit
def test_case_instantiation() -> None:
    """Construct ``Case`` with required FK and payload."""
    cid = uuid.uuid4()
    c = Case(
        id=cid,
        bias_type_id=1,
        parametric_payload={},
        source="seed",
        status="active",
        variant=0,
        rating_sum=0,
        rating_count=0,
    )
    assert c.bias_type_id == 1
    assert c.source == "seed"
    assert c.status == "active"


@pytest.mark.unit
def test_case_translation_instantiation() -> None:
    """Construct ``CaseTranslation`` with JSON options."""
    opts = [{"label": "A", "text": "One"}]
    t = CaseTranslation(
        case_id=uuid.uuid4(),
        locale="en",
        title="T",
        question="Q?",
        options=opts,
        correct_option=0,
        explanation="E",
        source_hash="deadbeef",
    )
    assert t.locale == "en"
    assert t.options == opts


@pytest.mark.unit
def test_ui_string_instantiation() -> None:
    """Construct ``UiString`` keyed by ``key``."""
    us = UiString(
        key="app_title",
        title="Cognitive Bias Tester",
        description="App name",
        source_hash="abc123",
    )
    assert us.key == "app_title"


@pytest.mark.unit
def test_ui_string_translation_instantiation() -> None:
    """Construct ``UiStringTranslation`` composite key."""
    tr = UiStringTranslation(
        key="app_title",
        locale="cs",
        source_hash="h",
        title_translated="Test",
        description_translated=None,
    )
    assert tr.locale == "cs"
    assert tr.description_translated is None


@pytest.mark.unit
def test_answer_event_instantiation() -> None:
    """Construct ``AnswerEvent`` with optional ``user_id``."""
    ev = AnswerEvent(
        case_id=uuid.uuid4(),
        chosen_option=2,
        is_correct=True,
    )
    assert ev.user_id is None
    assert ev.is_correct is True


@pytest.mark.unit
def test_rating_instantiation() -> None:
    """Construct ``Rating`` with star count."""
    r = Rating(case_id=uuid.uuid4(), stars=4)
    assert r.stars == 4


@pytest.mark.unit
def test_subscription_instantiation() -> None:
    """Construct ``Subscription``; ``stripe_sub_id`` is null until E060."""
    s = Subscription(user_id=uuid.uuid4(), status="inactive")
    assert s.stripe_sub_id is None
    assert s.status == "inactive"
