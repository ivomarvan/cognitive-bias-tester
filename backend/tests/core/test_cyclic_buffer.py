"""Tests for ``InMemoryCyclicBuffer`` stub."""

from __future__ import annotations

import uuid

import pytest

from src.core.cyclic_buffer import InMemoryCyclicBuffer


@pytest.mark.unit
async def test_insert_increases_size() -> None:
    """Inserting a new ID increases ``size``."""
    buf = InMemoryCyclicBuffer(capacity=10)
    await buf.insert(uuid.uuid4())
    assert await buf.size() == 1


@pytest.mark.unit
async def test_insert_duplicate_is_noop() -> None:
    """Duplicate UUID does not change size."""
    buf = InMemoryCyclicBuffer(capacity=10)
    uid = uuid.uuid4()
    await buf.insert(uid)
    await buf.insert(uid)
    assert await buf.size() == 1


@pytest.mark.unit
async def test_get_next_empty_returns_none() -> None:
    """Empty buffer yields ``None``."""
    buf = InMemoryCyclicBuffer(capacity=10)
    assert await buf.get_next(locale="en") is None


@pytest.mark.unit
async def test_get_next_cycles_round_robin() -> None:
    """``get_next`` repeats the insertion order indefinitely."""
    buf = InMemoryCyclicBuffer(capacity=10)
    ids = [uuid.uuid4() for _ in range(3)]
    for uid in ids:
        await buf.insert(uid)
    results = [await buf.get_next(locale="en") for _ in range(6)]
    assert results == ids + ids


@pytest.mark.unit
async def test_evict_worst_removes_excess() -> None:
    """Tail eviction shrinks to ``capacity``."""
    buf = InMemoryCyclicBuffer(capacity=2)
    for _ in range(3):
        await buf.insert(uuid.uuid4())
    evicted = await buf.evict_worst()
    assert evicted == 1
    assert await buf.size() == 2


@pytest.mark.unit
async def test_evict_worst_within_capacity_is_noop() -> None:
    """No eviction when already under cap."""
    buf = InMemoryCyclicBuffer(capacity=5)
    await buf.insert(uuid.uuid4())
    evicted = await buf.evict_worst()
    assert evicted == 0
    assert await buf.size() == 1
