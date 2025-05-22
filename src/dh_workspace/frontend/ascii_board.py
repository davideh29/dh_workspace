"""ASCII chessboard drawing utilities."""

from __future__ import annotations

from pathlib import Path

from ..utils.config import CONFIG


def draw_empty_board(width: int | None = None, height: int | None = None) -> str:
    """Return a simple ASCII representation of an empty chessboard."""
    w = width or CONFIG.board_width
    h = height or CONFIG.board_height

    top_border = " " + " _" * w
    lines = [top_border]
    for _ in range(h):
        line = "|" + "_|" * w
        lines.append(line)
    return "\n".join(lines)


def save_board(text: str, path: str | Path) -> None:
    """Write ``text`` representing a board to ``path``."""
    Path(path).write_text(text)
