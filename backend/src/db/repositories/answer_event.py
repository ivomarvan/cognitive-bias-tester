"""Repository for ``AnswerEvent`` rows."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.answer_event import AnswerEvent
from src.db.repositories.base import Repository


class AnswerEventRepository(Repository[AnswerEvent]):
    """Data access for answer analytics events."""

    model_cls: ClassVar[type[AnswerEvent]] = AnswerEvent

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def list_by_user(self, user_id: UUID, limit: int = 100) -> list[AnswerEvent]:
        """Return recent answer events for a user, newest first.

        Args:
            user_id: Filter by ``AnswerEvent.user_id``.
            limit: Max rows (default 100).

        Returns:
            Ordered list (possibly empty).

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = (
            select(AnswerEvent)
            .where(AnswerEvent.user_id == user_id)
            .order_by(AnswerEvent.answered_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
