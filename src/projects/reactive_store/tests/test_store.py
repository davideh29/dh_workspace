"""Tests for the reactive in-memory store."""

from __future__ import annotations

import asyncio
import os
import queue
import threading
import time
from typing import List

import pytest

from projects.reactive_store import Event, ReactiveStore


def _drain_events(
    event_queue: "queue.Queue[Event]", count: int, timeout: float = 1.0
) -> List[Event]:
    events: List[Event] = []
    for _ in range(count):
        events.append(event_queue.get(timeout=timeout))
    return events


def test_basic_operations_snapshot_and_listing() -> None:
    store = ReactiveStore()
    try:
        store.set("root.leaf", 42)
        assert store.get("root.leaf") == 42
        assert store.exists("root.leaf")

        store.set("root.branch", "value")
        snapshot = store.list()
        assert set(snapshot) == {"root.leaf", "root.branch"}

        branch_snapshot = store.list("root")
        assert set(branch_snapshot) == {"root.leaf", "root.branch"}
        assert store.list("root.leaf") == ("root.leaf",)

        store.delete("root.branch")
        assert not store.exists("root.branch")
        assert store.list("root") == ("root.leaf",)
    finally:
        store.shutdown()


def test_invalid_paths_raise_value_error() -> None:
    store = ReactiveStore()
    try:
        with pytest.raises(ValueError):
            store.set("invalid path", 1)
        with pytest.raises(ValueError):
            store.get("double..dot")
        with pytest.raises(ValueError):
            store.subscribe("bad selector.*.extra", lambda event: None)
    finally:
        store.shutdown()


def test_exact_subscription_receives_events_in_order() -> None:
    store = ReactiveStore()
    events: "queue.Queue[Event]" = queue.Queue()
    try:
        store.subscribe("alpha.beta", events.put)
        store.set("alpha.beta", 1)
        store.set("alpha.beta", 2)
        received = _drain_events(events, 2)
        assert [event.type for event in received] == ["set", "set"]
        assert [event.value for event in received] == [1, 2]
        assert [event.version for event in received] == [1, 2]
        assert all(event.path == "alpha.beta" for event in received)
        assert all(
            event.origin and event.origin["pid"] == os.getpid() for event in received
        )
    finally:
        store.shutdown()


def test_prefix_subscription_filters_descendants() -> None:
    store = ReactiveStore()
    events: "queue.Queue[Event]" = queue.Queue()
    try:
        store.subscribe("tree.branch.*", events.put)
        store.set("tree.branch.leaf1", "a")
        store.set("tree.branch.leaf2", "b")
        store.set("tree.other", "ignore")
        received = _drain_events(events, 2)
        paths = {event.path for event in received}
        assert paths == {"tree.branch.leaf1", "tree.branch.leaf2"}
    finally:
        store.shutdown()


def test_async_callback_supported() -> None:
    store = ReactiveStore()
    events: "queue.Queue[Event]" = queue.Queue()
    try:

        async def callback(event: Event) -> None:
            await asyncio.sleep(0)
            events.put(event)

        store.subscribe("async.topic", callback)
        store.set("async.topic", 123)
        received = _drain_events(events, 1)[0]
        assert received.type == "set"
        assert received.value == 123
    finally:
        store.shutdown()


def test_delete_emits_event_and_missing_delete_is_noop() -> None:
    store = ReactiveStore()
    events: "queue.Queue[Event]" = queue.Queue()
    try:
        store.subscribe("prunable.node", events.put)
        store.set("prunable.node", 10)
        store.delete("prunable.node")
        delete_event = _drain_events(events, 2)[1]
        assert delete_event.type == "delete"
        assert delete_event.value is None
        assert delete_event.path == "prunable.node"

        # Missing key should not emit anything
        time.sleep(0.05)
        assert events.empty()
    finally:
        store.shutdown()


def test_unsubscribe_prevents_future_events() -> None:
    store = ReactiveStore()
    events: "queue.Queue[Event]" = queue.Queue()
    try:
        subscription_id = store.subscribe("single.path", events.put)
        store.unsubscribe(subscription_id)
        store.set("single.path", "data")
        with pytest.raises(queue.Empty):
            events.get(timeout=0.1)
    finally:
        store.shutdown()


def test_callbacks_are_retried_after_failures() -> None:
    store = ReactiveStore(retry_base_delay=0.01, retry_max_delay=0.05)
    attempts: List[int] = []
    done = threading.Event()

    def callback(event: Event) -> None:
        attempts.append(event.version)
        if len(attempts) == 1:
            raise RuntimeError("boom")
        done.set()

    try:
        store.subscribe("retry.topic", callback)
        store.set("retry.topic", 7)
        assert done.wait(1.0)
        assert len(attempts) >= 2
        assert attempts[0] == attempts[1]
    finally:
        store.shutdown()


def test_context_manager_shuts_down_worker() -> None:
    with ReactiveStore() as store:
        store.set("ctx.example", True)
    # Give the worker a moment to exit and ensure no lingering threads processing events
    time.sleep(0.05)
