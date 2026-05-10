"""Repository for ``User`` rows."""

from __future__ import annotations

from typing import ClassVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User
from src.db.repositories.base import Repository


class UserRepository(Repository[User]):
    """Data access for application users."""

    model_cls: ClassVar[type[User]] = User

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with the given unique email, if any.

        Args:
            email: Login email address.

        Returns:
            ``User`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
