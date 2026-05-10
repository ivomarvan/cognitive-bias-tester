"""Generic async repository base (Pattern: Repository / GoF DAO variant)."""

from __future__ import annotations

from typing import ClassVar, Generic, TypeVar, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import Base as DeclarativeBase

ModelT = TypeVar("ModelT", bound=DeclarativeBase)


class Repository(Generic[ModelT]):
    """Generic async repository providing standard CRUD operations.

    Subclasses must set ``model_cls`` to the mapped ORM class.
    """

    model_cls: ClassVar[type[DeclarativeBase]]

    def __init__(self, session: AsyncSession) -> None:
        """Store the async session used for all operations in this repository.

        Args:
            session: Request-scoped ``AsyncSession``; the caller owns commits.

        Raises:
            None — this constructor does not touch the database.
        """
        self._session = session

    async def get_by_id(self, pk: UUID | int | str | tuple[str, str]) -> ModelT | None:
        """Load one row by primary key (scalar or composite tuple for text+locale).

        Args:
            pk: Primary key value accepted by ``AsyncSession.get``.

        Returns:
            The mapped instance if found, otherwise ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On underlying driver failures.
        """
        row = await self._session.get(self.model_cls, pk)
        return cast(ModelT | None, row)

    async def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        """Return up to ``limit`` rows starting at ``offset`` (unordered).

        Args:
            limit: Maximum rows to return (default 100).
            offset: Number of rows to skip.

        Returns:
            List of instances (possibly empty).

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On underlying driver failures.
        """
        stmt = select(self.model_cls).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return cast(list[ModelT], list(result.scalars().all()))

    async def add(self, instance: ModelT) -> ModelT:
        """Persist ``instance`` in the current transaction and flush.

        Args:
            instance: New ORM instance to insert.

        Returns:
            The same instance with server-generated fields populated after flush.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On constraint violations or driver errors.
        """
        self._session.add(instance)
        await self._session.flush()
        return instance

    async def delete(self, instance: ModelT) -> None:
        """Delete ``instance`` and flush; caller commits the transaction.

        Args:
            instance: ORM instance to remove.

        Returns:
            ``None``.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: On underlying driver failures.
        """
        await self._session.delete(instance)
        await self._session.flush()
