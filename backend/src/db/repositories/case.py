"""Repository for ``Case`` rows."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.case import Case
from src.db.repositories.base import Repository


class CaseRepository(Repository[Case]):
    """Data access for playable bias cases."""

    model_cls: ClassVar[type[Case]] = Case

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_by_bias_type(self, bias_type_id: int, status: str = "active") -> list[Case]:
        """List cases for a bias type filtered by lifecycle ``status``.

        Args:
            bias_type_id: Foreign key to ``bias_type.id``.
            status: Case status filter (default ``active``).

        Returns:
            All matching cases (possibly empty).

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = (
            select(Case)
            .where(Case.bias_type_id == bias_type_id, Case.status == status)
            .order_by(Case.created_at)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_rating(self, case_id: UUID, stars: int) -> None:
        """Atomically add ``stars`` to aggregates and bump ``rating_count``.

        Args:
            case_id: Target case primary key.
            stars: Star count to add (caller enforces 1–5 at higher layers).

        Returns:
            ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
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
