"""Utility functions for the core package."""

from __future__ import annotations


def index_to_letters(index: int) -> str:
    """Return the alphabetical representation for ``index``.

    The index is one-based (1 -> "A"). Supports values beyond ``Z`` using
    repeated letters similar to Excel column naming.
    """
    if index < 1:
        raise ValueError("index must be >= 1")

    result = ""
    while index > 0:
        index -= 1
        result = chr(ord("A") + index % 26) + result
        index //= 26
    return result
