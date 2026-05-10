"""Repository for ``Rating`` rows."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.rating import Rating
from src.db.repositories.base import Repository


class RatingRepository(Repository[Rating]):
    """Data access for per-user case star ratings."""

    model_cls: ClassVar[type[Rating]] = Rating

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_by_user_and_case(self, user_id: UUID, case_id: UUID) -> Rating | None:
        """Return a rating row for the user+case pair, if it exists.

        Args:
            user_id: Rater (nullable column; match exact UUID).
            case_id: Target case id.

        Returns:
            ``Rating`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(Rating).where(
            Rating.user_id == user_id,
            Rating.case_id == case_id,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
