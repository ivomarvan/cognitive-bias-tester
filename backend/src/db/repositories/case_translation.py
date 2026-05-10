"""Repository for ``CaseTranslation`` rows."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.case_translation import CaseTranslation
from src.db.repositories.base import Repository


class CaseTranslationRepository(Repository[CaseTranslation]):
    """Data access for localized case copy."""

    model_cls: ClassVar[type[CaseTranslation]] = CaseTranslation

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_by_case_and_locale(self, case_id: UUID, locale: str) -> CaseTranslation | None:
        """Return translation for one case and locale, if present.

        Args:
            case_id: Parent ``Case`` id.
            locale: BCP-47 or app locale tag.

        Returns:
            ``CaseTranslation`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(CaseTranslation).where(
            CaseTranslation.case_id == case_id,
            CaseTranslation.locale == locale,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
