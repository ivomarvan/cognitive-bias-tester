"""Unit tests for idempotent ``run_seed_with_repos`` (mocked repositories)."""

from __future__ import annotations

import uuid
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from src.db.models.bias_type import BiasType
from src.db.models.case import Case
from src.db.models.ui_string import UiString
from src.db.repositories.bias_type import BiasTypeRepository
from src.db.repositories.case import CaseRepository
from src.db.repositories.case_translation import CaseTranslationRepository
from src.db.repositories.ui_string import UiStringRepository
from src.db.seed.seed import compute_source_hash, load_fixtures, run_seed_with_repos

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "src" / "db" / "seed"

BIAS_IDS = {
    "anchoring": 1,
    "framing": 2,
    "loss_aversion": 3,
    "confirmation_bias": 4,
    "sunk_cost": 5,
}


def _existing_bias(slug: str) -> BiasType:
    """Build a persisted-looking bias row with deterministic PK."""
    return BiasType(
        id=BIAS_IDS[slug],
        slug=slug,
        name_en="n",
        description_en="d",
    )


@pytest.mark.unit
async def test_seed_inserts_bias_types_on_first_run() -> None:
    """First seed calls ``BiasTypeRepository.add`` once per fixture row."""
    bias_data, case_data, ui_data = load_fixtures(FIXTURE_DIR)
    bias_repo = AsyncMock(spec=BiasTypeRepository)
    case_repo = AsyncMock(spec=CaseRepository)
    case_tr_repo = AsyncMock(spec=CaseTranslationRepository)
    ui_repo = AsyncMock(spec=UiStringRepository)

    bias_repo.get_by_slug = AsyncMock(return_value=None)
    next_id = 1

    async def bias_add(instance: BiasType) -> BiasType:
        nonlocal next_id
        instance.id = next_id
        next_id += 1
        return instance

    bias_repo.add = AsyncMock(side_effect=bias_add)
    case_repo.get_by_bias_type = AsyncMock(return_value=[])

    async def case_add(instance: Case) -> Case:
        instance.id = uuid.uuid4()
        return instance

    case_repo.add = AsyncMock(side_effect=case_add)
    case_tr_repo.add = AsyncMock(side_effect=lambda x: x)
    ui_repo.get_by_id = AsyncMock(return_value=None)
    ui_repo.add = AsyncMock(side_effect=lambda x: x)

    stats = await run_seed_with_repos(
        bias_repo, case_repo, case_tr_repo, ui_repo, bias_data, case_data, ui_data
    )

    assert stats.bias_types_inserted == 5
    assert stats.bias_types_skipped == 0
    assert bias_repo.add.await_count == 5


@pytest.mark.unit
async def test_seed_skips_existing_bias_types() -> None:
    """When slugs exist, seed does not insert bias types again."""
    bias_data, case_data, ui_data = load_fixtures(FIXTURE_DIR)
    bias_repo = AsyncMock(spec=BiasTypeRepository)
    case_repo = AsyncMock(spec=CaseRepository)
    case_tr_repo = AsyncMock(spec=CaseTranslationRepository)
    ui_repo = AsyncMock(spec=UiStringRepository)

    bias_repo.get_by_slug = AsyncMock(side_effect=lambda slug: _existing_bias(str(slug)))
    case_repo.get_by_bias_type = AsyncMock(return_value=[])

    async def case_add(instance: Case) -> Case:
        instance.id = uuid.uuid4()
        return instance

    case_repo.add = AsyncMock(side_effect=case_add)
    case_tr_repo.add = AsyncMock(side_effect=lambda x: x)
    ui_repo.get_by_id = AsyncMock(return_value=None)
    ui_repo.add = AsyncMock(side_effect=lambda x: x)

    stats = await run_seed_with_repos(
        bias_repo, case_repo, case_tr_repo, ui_repo, bias_data, case_data, ui_data
    )

    assert stats.bias_types_skipped == 5
    assert stats.bias_types_inserted == 0
    bias_repo.add.assert_not_called()


@pytest.mark.unit
async def test_seed_inserts_25_cases() -> None:
    """All gold-standard cases trigger ``CaseRepository.add`` once."""
    bias_data, case_data, ui_data = load_fixtures(FIXTURE_DIR)
    assert len(case_data) == 25

    bias_repo = AsyncMock(spec=BiasTypeRepository)
    case_repo = AsyncMock(spec=CaseRepository)
    case_tr_repo = AsyncMock(spec=CaseTranslationRepository)
    ui_repo = AsyncMock(spec=UiStringRepository)

    bias_repo.get_by_slug = AsyncMock(side_effect=lambda slug: _existing_bias(str(slug)))
    case_repo.get_by_bias_type = AsyncMock(return_value=[])

    async def case_add(instance: Case) -> Case:
        instance.id = uuid.uuid4()
        return instance

    case_repo.add = AsyncMock(side_effect=case_add)
    case_tr_repo.add = AsyncMock(side_effect=lambda x: x)
    ui_repo.get_by_id = AsyncMock(return_value=None)
    ui_repo.add = AsyncMock(side_effect=lambda x: x)

    await run_seed_with_repos(
        bias_repo, case_repo, case_tr_repo, ui_repo, bias_data, case_data, ui_data
    )

    assert case_repo.add.await_count == 25
    assert case_tr_repo.add.await_count == 25


@pytest.mark.unit
async def test_seed_computes_source_hash_for_ui_strings() -> None:
    """``UiString.source_hash`` is a non-empty digest derived from content."""
    bias_data, case_data, ui_data = load_fixtures(FIXTURE_DIR)
    bias_repo = AsyncMock(spec=BiasTypeRepository)
    case_repo = AsyncMock(spec=CaseRepository)
    case_tr_repo = AsyncMock(spec=CaseTranslationRepository)
    ui_repo = AsyncMock(spec=UiStringRepository)

    bias_repo.get_by_slug = AsyncMock(side_effect=lambda slug: _existing_bias(str(slug)))
    case_repo.get_by_bias_type = AsyncMock(return_value=[])

    async def case_add(instance: Case) -> Case:
        instance.id = uuid.uuid4()
        return instance

    case_repo.add = AsyncMock(side_effect=case_add)
    case_tr_repo.add = AsyncMock(side_effect=lambda x: x)
    ui_repo.get_by_id = AsyncMock(return_value=None)
    ui_repo.add = AsyncMock(side_effect=lambda x: x)

    await run_seed_with_repos(
        bias_repo, case_repo, case_tr_repo, ui_repo, bias_data, case_data, ui_data
    )

    assert ui_repo.add.await_count == len(ui_data)
    first: UiString = ui_repo.add.await_args_list[0].args[0]
    assert first.source_hash == compute_source_hash(first.key, first.title, first.description)
    assert len(first.source_hash) == 64
