"""Idempotent database seed script.

Usage: ``python -m src.db.seed.seed``

Loads JSON fixtures next to this module and inserts rows via repositories. Skips
rows that already exist so the script can run repeatedly without duplicates.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.db.models.bias_type import BiasType
from src.db.models.case import Case
from src.db.models.case_translation import CaseTranslation
from src.db.models.ui_string import UiString
from src.db.repositories.bias_type import BiasTypeRepository
from src.db.repositories.case import CaseRepository
from src.db.repositories.case_translation import CaseTranslationRepository
from src.db.repositories.ui_string import UiStringRepository
from src.db.session import async_session

logger = logging.getLogger(__name__)


@dataclass
class SeedStats:
    """Counters for logging seed outcomes."""

    bias_types_inserted: int = 0
    bias_types_skipped: int = 0
    cases_inserted: int = 0
    cases_skipped: int = 0
    ui_strings_inserted: int = 0
    ui_strings_skipped: int = 0


def compute_source_hash(key: str, title: str, description: str) -> str:
    """Return SHA-256 hex of canonical English source fields for a UI key.

    Args:
        key: Stable string identifier.
        title: English title text.
        description: English description text.

    Returns:
        Lowercase hex digest string.

    Raises:
        None.
    """
    payload = f"{key}|{title}|{description}".encode()
    return hashlib.sha256(payload).hexdigest()


def compute_case_translation_hash(record: dict[str, Any]) -> str:
    """Hash immutable bilingual content for ``CaseTranslation.source_hash``.

    Args:
        record: One case dict from ``cases.json``.

    Returns:
        Lowercase hex digest string.

    Raises:
        KeyError: If required keys are missing.
    """
    canonical = {
        "title": record["title"],
        "question": record["question"],
        "options": record["options"],
        "correct_option": record["correct_option"],
        "explanation": record["explanation"],
        "locale": record["locale"],
    }
    blob = json.dumps(canonical, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(blob).hexdigest()


def load_fixtures(
    directory: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Parse the three fixture JSON files.

    Args:
        directory: Folder that contains ``bias_types.json``, ``cases.json``,
            ``ui_strings.json``.

    Returns:
        Tuple of bias list, case list, UI string dict.

    Raises:
        FileNotFoundError: If any fixture file is missing.
        json.JSONDecodeError: If a file is not valid JSON.
    """
    bias_raw = (directory / "bias_types.json").read_text(encoding="utf-8")
    cases_raw = (directory / "cases.json").read_text(encoding="utf-8")
    ui_raw = (directory / "ui_strings.json").read_text(encoding="utf-8")
    bias_data = json.loads(bias_raw)
    case_data = json.loads(cases_raw)
    ui_data = json.loads(ui_raw)
    if (
        not isinstance(bias_data, list)
        or not isinstance(case_data, list)
        or not isinstance(ui_data, dict)
    ):
        raise TypeError("Unexpected fixture JSON top-level types")
    return bias_data, case_data, ui_data


async def run_seed_with_repos(
    bias_repo: BiasTypeRepository,
    case_repo: CaseRepository,
    case_tr_repo: CaseTranslationRepository,
    ui_repo: UiStringRepository,
    bias_records: list[dict[str, Any]],
    case_records: list[dict[str, Any]],
    ui_records: dict[str, Any],
) -> SeedStats:
    """Insert fixture rows using the supplied repositories (testable entry point).

    Args:
        bias_repo: Repository for ``BiasType``.
        case_repo: Repository for ``Case``.
        case_tr_repo: Repository for ``CaseTranslation``.
        ui_repo: Repository for ``UiString``.
        bias_records: Parsed ``bias_types.json``.
        case_records: Parsed ``cases.json``.
        ui_records: Parsed ``ui_strings.json``.

    Returns:
        Counters describing inserted vs skipped rows.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: On unexpected database errors.
    """
    stats = SeedStats()

    slug_to_id: dict[str, int] = {}
    for row in bias_records:
        slug = str(row["slug"])
        existing = await bias_repo.get_by_slug(slug)
        if existing is not None:
            stats.bias_types_skipped += 1
            slug_to_id[slug] = existing.id
            continue
        instance = BiasType(
            slug=slug,
            name_en=str(row["name_en"]),
            description_en=str(row["description_en"]),
        )
        await bias_repo.add(instance)
        stats.bias_types_inserted += 1
        slug_to_id[slug] = instance.id

    for row in case_records:
        slug = str(row["bias_type_slug"])
        bias_id = slug_to_id[slug]
        variant = int(row["variant"])
        existing_cases = await case_repo.get_by_bias_type(bias_id, status="active")
        if variant in {c.variant for c in existing_cases}:
            stats.cases_skipped += 1
            continue
        case = Case(
            bias_type_id=bias_id,
            variant=variant,
            parametric_payload=dict(row["parametric_payload"]),
        )
        await case_repo.add(case)
        stats.cases_inserted += 1
        tr = CaseTranslation(
            case_id=case.id,
            locale=str(row["locale"]),
            title=str(row["title"]),
            question=str(row["question"]),
            options=list(row["options"]),
            correct_option=int(row["correct_option"]),
            explanation=str(row["explanation"]),
            source_hash=compute_case_translation_hash(row),
        )
        await case_tr_repo.add(tr)

    for key, meta in ui_records.items():
        existing_ui = await ui_repo.get_by_id(key)
        if existing_ui is not None:
            stats.ui_strings_skipped += 1
            continue
        title = str(meta["title"])
        description = str(meta["description"])
        ui_row = UiString(
            key=key,
            title=title,
            description=description,
            source_hash=compute_source_hash(key, title, description),
        )
        await ui_repo.add(ui_row)
        stats.ui_strings_inserted += 1

    return stats


async def seed() -> None:
    """Load fixtures from disk and run one transactional seed pass.

    Args:
        None.

    Returns:
        ``None``.

    Raises:
        FileNotFoundError: If fixtures are missing.
        sqlalchemy.exc.SQLAlchemyError: On database errors.
    """
    fixture_dir = Path(__file__).resolve().parent
    bias_records, case_records, ui_records = load_fixtures(fixture_dir)

    async with async_session() as session, session.begin():
        stats = await run_seed_with_repos(
            BiasTypeRepository(session),
            CaseRepository(session),
            CaseTranslationRepository(session),
            UiStringRepository(session),
            bias_records,
            case_records,
            ui_records,
        )

    logger.info(
        "seed complete bias_types inserted=%s skipped=%s cases inserted=%s skipped=%s "
        "ui_strings inserted=%s skipped=%s",
        stats.bias_types_inserted,
        stats.bias_types_skipped,
        stats.cases_inserted,
        stats.cases_skipped,
        stats.ui_strings_inserted,
        stats.ui_strings_skipped,
    )


def main() -> None:
    """Configure logging and run the async seed coroutine."""
    logging.basicConfig(level=logging.INFO)
    asyncio.run(seed())


if __name__ == "__main__":
    main()
