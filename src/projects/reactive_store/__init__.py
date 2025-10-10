"""Reactive in-memory hierarchical key-value store with async callbacks."""

from __future__ import annotations

import asyncio
import inspect
import logging
import os
import queue
import re
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Iterable, Optional

__all__ = ["ReactiveStore", "Event", "SubscriptionId"]

SubscriptionId = str

_PATH_SEGMENT_RE = re.compile(r"^[A-Za-z0-9_]+$")
_MISSING = object()


@dataclass(frozen=True)
class Event:
    """Payload delivered to subscribers."""

    type: str
    path: str
    value: Any | None = None
    timestamp: float = 0.0
    version: int = 0
    origin: Dict[str, int] | None = None


@dataclass
class _Subscription:
    selector: str
    callback: Callable[[Event], Awaitable[None] | None | Any]
    match_exact: bool
    prefix: Optional[str]
    retry_on_error: bool

    def matches(self, path: str) -> bool:
        if self.match_exact:
            return path == self.selector
        if self.prefix is None:
            return True
        return path.startswith(self.prefix)


@dataclass
class _QueuedEvent:
    event: Event
    subscription_id: SubscriptionId
    subscription: _Subscription
    attempt: int = 0
    delay: float = 0.0


class ReactiveStore:
    """Thread-safe hierarchical key-value store with reactive callbacks."""

    def __init__(
        self,
        *,
        logger: Optional[logging.Logger] = None,
        retry_base_delay: float = 0.05,
        retry_max_delay: float = 1.0,
    ) -> None:
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._version = 0
        self._subscriptions: Dict[SubscriptionId, _Subscription] = {}
        self._queue: "queue.Queue[_QueuedEvent | None]" = queue.Queue()
        self._stop_event = threading.Event()
        self._logger = logger or logging.getLogger(__name__)
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay
        self._worker = threading.Thread(
            target=self._worker_loop, name="ReactiveStoreWorker", daemon=True
        )
        self._worker.start()

    # ------------------------------------------------------------------
    # Public API
    def set(self, path: str, value: Any) -> None:
        normalized = self._validate_path(path)
        with self._lock:
            self._data[normalized] = value
            event = self._build_event("set", normalized, value)
        self._enqueue_event(event)

    def get(self, path: str) -> Any | None:
        normalized = self._validate_path(path)
        with self._lock:
            return self._data.get(normalized)

    def exists(self, path: str) -> bool:
        normalized = self._validate_path(path)
        with self._lock:
            return normalized in self._data

    def delete(self, path: str) -> None:
        normalized = self._validate_path(path)
        with self._lock:
            value = self._data.pop(normalized, _MISSING)
            if value is _MISSING:
                return
            event = self._build_event("delete", normalized, None)
        self._enqueue_event(event)

    def list(self, prefix: str | None = None) -> Iterable[str]:
        if prefix is not None:
            normalized = self._validate_selector(prefix, allow_wildcard=False)
        else:
            normalized = None
        with self._lock:
            keys = tuple(self._data.keys())
        if normalized is None:
            return keys
        dotted_prefix = f"{normalized}."
        return tuple(
            key for key in keys if key == normalized or key.startswith(dotted_prefix)
        )

    def subscribe(
        self,
        selector: str,
        callback: Callable[[Event], Awaitable[None] | None | Any],
        *,
        retry_on_error: bool = True,
    ) -> SubscriptionId:
        subscription = self._create_subscription(
            selector, callback, retry_on_error=retry_on_error
        )
        subscription_id = str(uuid.uuid4())
        with self._lock:
            self._subscriptions[subscription_id] = subscription
        return subscription_id

    def unsubscribe(self, subscription_id: SubscriptionId) -> None:
        with self._lock:
            self._subscriptions.pop(subscription_id, None)

    def shutdown(self) -> None:
        """Stop the worker thread and drain events for clean shutdown."""

        self._stop_event.set()
        self._queue.put(None)
        self._worker.join(timeout=5.0)
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    # ------------------------------------------------------------------
    # Internal helpers
    def _validate_path(self, path: str) -> str:
        if not isinstance(path, str) or not path:
            raise ValueError("Path must be a non-empty string")
        segments = path.split(".")
        if any(not _PATH_SEGMENT_RE.fullmatch(segment) for segment in segments):
            raise ValueError(f"Invalid path: {path!r}")
        return path

    def _validate_selector(self, selector: str, *, allow_wildcard: bool) -> str:
        if not isinstance(selector, str) or not selector:
            raise ValueError("Selector must be a non-empty string")
        if allow_wildcard and selector == "*":
            return ""
        if allow_wildcard and selector.endswith(".*"):
            base = selector[:-2]
            self._validate_path(base)
            return base + "."
        self._validate_path(selector)
        return selector

    def _create_subscription(
        self,
        selector: str,
        callback: Callable[[Event], Awaitable[None] | None | Any],
        *,
        retry_on_error: bool,
    ) -> _Subscription:
        if not callable(callback):
            raise TypeError("Callback must be callable")
        if selector == "*":
            return _Subscription(
                selector=selector,
                callback=callback,
                match_exact=False,
                prefix=None,
                retry_on_error=retry_on_error,
            )
        if selector.endswith(".*"):
            prefix_base = self._validate_selector(selector, allow_wildcard=True)
            return _Subscription(
                selector=selector,
                callback=callback,
                match_exact=False,
                prefix=prefix_base,
                retry_on_error=retry_on_error,
            )
        normalized = self._validate_selector(selector, allow_wildcard=False)
        return _Subscription(
            selector=normalized,
            callback=callback,
            match_exact=True,
            prefix=None,
            retry_on_error=retry_on_error,
        )

    def _build_event(self, event_type: str, path: str, value: Any | None) -> Event:
        with self._lock:
            self._version += 1
            version = self._version
        timestamp = time.monotonic()
        origin = {"pid": os.getpid(), "tid": threading.get_ident()}
        return Event(
            type=event_type,
            path=path,
            value=value,
            timestamp=timestamp,
            version=version,
            origin=origin,
        )

    def _enqueue_event(self, event: Event) -> None:
        with self._lock:
            items = list(self._subscriptions.items())
        for subscription_id, subscription in items:
            if subscription.matches(event.path):
                self._queue.put(
                    _QueuedEvent(
                        event=event,
                        subscription_id=subscription_id,
                        subscription=subscription,
                        attempt=0,
                        delay=self._retry_base_delay,
                    )
                )

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                queued = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue
            if queued is None:
                break
            self._dispatch(queued)

    def _dispatch(self, queued: _QueuedEvent) -> None:
        subscription = queued.subscription
        event = queued.event
        delay = max(self._retry_base_delay, min(queued.delay, self._retry_max_delay))
        attempt = queued.attempt + 1
        try:
            result = subscription.callback(event)
            if inspect.isawaitable(result):
                asyncio.run(self._await_result(result))
        except Exception:  # pragma: no cover - logged and retried
            self._logger.exception(
                "ReactiveStore callback failed",
                extra={"subscription": subscription.selector, "attempt": attempt},
            )
            if not subscription.retry_on_error:
                return
            time.sleep(delay)
            next_delay = min(delay * 2, self._retry_max_delay)
            self._queue.put(
                _QueuedEvent(
                    event=event,
                    subscription_id=queued.subscription_id,
                    subscription=subscription,
                    attempt=attempt,
                    delay=next_delay,
                )
            )
        else:
            return

    async def _await_result(self, result: Awaitable[Any]) -> None:
        await result

    # Context manager helpers
    def __enter__(self) -> "ReactiveStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.shutdown()
