"""Repository for ``BiasType`` rows."""

from __future__ import annotations

from typing import ClassVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.bias_type import BiasType
from src.db.repositories.base import Repository


class BiasTypeRepository(Repository[BiasType]):
    """Data access for bias taxonomy entries."""

    model_cls: ClassVar[type[BiasType]] = BiasType

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_by_slug(self, slug: str) -> BiasType | None:
        """Return the bias type with the given URL slug, if any.

        Args:
            slug: Unique slug string (e.g. ``anchoring``).

        Returns:
            Matching ``BiasType`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(BiasType).where(BiasType.slug == slug)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
