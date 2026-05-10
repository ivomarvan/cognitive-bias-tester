"""Repository for ``UiString`` and ``UiStringTranslation`` access."""

from __future__ import annotations

from typing import ClassVar

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.ui_string import UiString
from src.db.models.ui_string_translation import UiStringTranslation
from src.db.repositories.base import Repository


class UiStringRepository(Repository[UiString]):
    """Data access for UI source keys and their locale translations."""

    model_cls: ClassVar[type[UiString]] = UiString

    def __init__(self, session: AsyncSession) -> None:
        """Initialize with an async session.

        Args:
            session: Active ``AsyncSession`` for this unit of work.

        Raises:
            None.
        """
        super().__init__(session)

    async def get_all_keys(self) -> list[UiString]:
        """Return every ``UiString`` row ordered by key.

        Args:
            None.

        Returns:
            Ordered list of canonical UI strings.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(UiString).order_by(UiString.key)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_translation(self, key: str, locale: str) -> UiStringTranslation | None:
        """Return one translation row for ``key`` and ``locale``.

        Args:
            key: ``UiString`` primary key.
            locale: Target locale tag.

        Returns:
            ``UiStringTranslation`` or ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = select(UiStringTranslation).where(
            UiStringTranslation.key == key,
            UiStringTranslation.locale == locale,
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_with_translation(
        self, locale: str
    ) -> list[tuple[UiString, UiStringTranslation | None]]:
        """Join all ``UiString`` rows with optional translation for ``locale``.

        Args:
            locale: Locale tag for the left outer join.

        Returns:
            Pairs of ``(UiString, translation or None)`` in key order.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures.
        """
        stmt = (
            select(UiString, UiStringTranslation)
            .outerjoin(
                UiStringTranslation,
                (UiStringTranslation.key == UiString.key) & (UiStringTranslation.locale == locale),
            )
            .order_by(UiString.key)
        )
        result = await self._session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

    async def upsert_translation(
        self,
        key: str,
        locale: str,
        title_translated: str,
        description_translated: str | None,
        source_hash: str,
    ) -> UiStringTranslation:
        """Insert or update a translation row using PostgreSQL ``ON CONFLICT``.

        Args:
            key: ``UiString`` foreign key.
            locale: Locale for the composite primary key.
            title_translated: Translated title text.
            description_translated: Optional translated description.
            source_hash: Hash of upstream source for staleness checks.

        Returns:
            The persisted ``UiStringTranslation`` (returning row).

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On driver failures or FK violations.
        """
        stmt = (
            pg_insert(UiStringTranslation)
            .values(
                key=key,
                locale=locale,
                title_translated=title_translated,
                description_translated=description_translated,
                source_hash=source_hash,
            )
            .on_conflict_do_update(
                index_elements=["key", "locale"],
                set_={
                    "title_translated": title_translated,
                    "description_translated": description_translated,
                    "source_hash": source_hash,
                },
            )
            .returning(UiStringTranslation)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
