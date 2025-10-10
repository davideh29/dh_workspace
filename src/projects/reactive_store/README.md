# Reactive Store

A lightweight, thread-safe key-value store that emits change notifications.
Keys are hierarchical dotted paths (for example `pipeline.stage.step`).

## Creating a store

```python
from projects.reactive_store import ReactiveStore

store = ReactiveStore()
```

The store starts a background worker thread to fan out events. Call
`store.shutdown()` when finished or use it as a context manager to shut down
automatically.

## Working with data

- `set(path, value)` records a value and emits a `set` event.
- `get(path)` retrieves the current value or `None` if it is missing.
- `exists(path)` returns a boolean indicating whether a value is stored.
- `delete(path)` removes a value. Deleting a missing key is a no-op and does not
  emit an event.
- `list(prefix=None)` returns a tuple of paths. With a prefix, only exact
  matches and descendants are returned.

Paths must be non-empty strings made from letters, numbers, or underscores
separated by dots. Invalid paths raise `ValueError`.

## Subscriptions

Use `subscribe(selector, callback)` to receive `Event` objects whenever
matching paths change. A selector can be:

- An exact path such as `"alpha.beta"`.
- A dotted prefix ending with `.*` to watch descendants, e.g. `"alpha.*"`.
- A single `*` to receive every event.

Callbacks can be synchronous or `async def`. Async callbacks are awaited in
the worker thread. The return value is ignored. To stop receiving events, call
`unsubscribe(subscription_id)`.

`Event` instances include:

- `type`: either `"set"` or `"delete"`.
- `path`: the full key that changed.
- `value`: the stored value for `set`, or `None` for `delete`.
- `version`: a monotonically increasing counter per store.
- `timestamp`: `time.monotonic()` when the event was created.
- `origin`: `{"pid": ..., "tid": ...}` showing the producing
  process/thread.

## Behavior notes

- Callbacks run sequentially inside the worker thread. Exceptions are logged and
  the event is retried with exponential backoff.
- Events are delivered in write order. Multiple subscribers can observe the same
  event.
- The store is safe to access from multiple threads.
- Always call `shutdown()` before process exit to flush the internal queue.
