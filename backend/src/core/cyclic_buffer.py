"""Cyclic buffer interface and in-memory stub (production DB in E030)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class CyclicBuffer(ABC):
    """Interface for the Case cyclic buffer — fully implemented in E030.

    The buffer holds a capped ordered set of active Case IDs. Cases are:
    inserted after LLM generation and judge validation (E030); retrieved
    round-robin by locale / bias type for Mode 1 serving; evicted by composite
    (rating_avg, age) score when the buffer exceeds capacity.
    """

    @abstractmethod
    async def insert(self, case_id: UUID) -> None:
        """Add a Case ID to the buffer. No-op if already present.

        Args:
            case_id: UUID of the Case to add.

        Returns:
            None.

        Raises:
            None from this interface; implementations may raise on I/O errors.
        """

    @abstractmethod
    async def get_next(
        self,
        locale: str,
        bias_type_slug: str | None = None,
    ) -> UUID | None:
        """Return the next Case ID for the given locale, or None if empty.

        Args:
            locale: IETF language tag of the requesting user.
            bias_type_slug: Optional filter — if set, only Cases of this bias type
                are eligible; ``None`` means any bias type.

        Returns:
            A Case UUID, or None when no eligible Cases are available.

        Raises:
            None from this interface; implementations may raise on errors.
        """

    @abstractmethod
    async def evict_worst(self) -> int:
        """Evict Cases until the buffer is at or below capacity.

        Eviction criterion (E030): lowest composite score of (rating_avg, recency).
        Stubs may use a simpler rule.

        Returns:
            Number of Case IDs removed.

        Raises:
            None from this interface; implementations may raise on errors.
        """

    @abstractmethod
    async def size(self) -> int:
        """Return the current number of Case IDs in the buffer.

        Args:
            None.

        Returns:
            Non-negative integer count.

        Raises:
            None from this interface; implementations may raise on errors.
        """


class InMemoryCyclicBuffer(CyclicBuffer):
    """Deterministic in-memory stub for unit tests — NOT for production use.

    Stores UUIDs in insertion order (list). ``get_next`` cycles round-robin
    over all stored IDs, ignoring locale and ``bias_type_slug``. ``evict_worst``
    removes items from the end of the insertion-order list until size ≤ capacity.
    """

    def __init__(self, capacity: int = 100) -> None:
        """Configure stub capacity and empty storage.

        Args:
            capacity: Maximum number of Case IDs retained after eviction.

        Returns:
            None.

        Raises:
            None.
        """
        self._capacity = capacity
        self._items: list[UUID] = []
        self._cursor = 0

    async def insert(self, case_id: UUID) -> None:
        """Append ``case_id`` if not already stored.

        Args:
            case_id: Case primary key to add.

        Returns:
            None.

        Raises:
            None.
        """
        if case_id not in self._items:
            self._items.append(case_id)

    async def get_next(
        self,
        locale: str,
        bias_type_slug: str | None = None,
    ) -> UUID | None:
        """Return the next ID in round-robin order (filters ignored).

        Args:
            locale: Ignored in this stub.
            bias_type_slug: Ignored in this stub.

        Returns:
            Next UUID or ``None`` if the buffer is empty.

        Raises:
            None.
        """
        if not self._items:
            return None
        item = self._items[self._cursor % len(self._items)]
        self._cursor += 1
        return item

    async def evict_worst(self) -> int:
        """Drop IDs from the tail until size is at most ``capacity``.

        Args:
            None.

        Returns:
            Count of removed IDs.

        Raises:
            None.
        """
        excess = max(0, len(self._items) - self._capacity)
        self._items = self._items[: len(self._items) - excess]
        return excess

    async def size(self) -> int:
        """Return stored ID count.

        Args:
            None.

        Returns:
            Number of Case IDs currently held.

        Raises:
            None.
        """
        return len(self._items)
