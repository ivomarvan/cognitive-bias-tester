"""Repository for ``Subscription`` rows."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.subscription import Subscription
from src.db.repositories.base import Repository


class SubscriptionRepository(Repository[Subscription]):
    """Data access for subscription billing rows."""

    model_cls: ClassVar[type[Subscription]] = Subscription

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_active_by_user(self, user_id: UUID) -> Subscription | None:
        """Return the user's subscription row with ``status`` ``active``, if any.

        Args:
            user_id: Owner user id.

        Returns:
            First matching ``Subscription`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = (
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
