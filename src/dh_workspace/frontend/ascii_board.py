"""ASCII chessboard drawing utilities."""

from __future__ import annotations

from pathlib import Path

from ..utils.config import CONFIG


_H_SEG = "━" * 3
_EMPTY_CELL = " " * 3


def draw_empty_board(width: int | None = None, height: int | None = None) -> str:
    """Return a Unicode board with empty squares."""

    w = width or CONFIG.board_width
    h = height or CONFIG.board_height

    top = "┏" + "┳".join(_H_SEG for _ in range(w)) + "┓"
    mid = "┣" + "╋".join(_H_SEG for _ in range(w)) + "┫"
    bottom = "┗" + "┻".join(_H_SEG for _ in range(w)) + "┛"

    lines = [top]
    for row in range(h):
        lines.append("┃" + "┃".join(_EMPTY_CELL for _ in range(w)) + "┃")
        if row < h - 1:
            lines.append(mid)
    lines.append(bottom)
    return "\n".join(lines)


def draw_board(board: "Chessboard") -> str:
    """Return a Unicode chessboard containing the pieces from ``board``."""

    from ..core.backend.pieces import PieceColor, PieceType

    unicode_map = {
        PieceColor.WHITE: {
            PieceType.PAWN: "♙",
            PieceType.KNIGHT: "♘",
            PieceType.BISHOP: "♗",
            PieceType.ROOK: "♖",
            PieceType.QUEEN: "♕",
            PieceType.KING: "♔",
        },
        PieceColor.BLACK: {
            PieceType.PAWN: "♟",
            PieceType.KNIGHT: "♞",
            PieceType.BISHOP: "♝",
            PieceType.ROOK: "♜",
            PieceType.QUEEN: "♛",
            PieceType.KING: "♚",
        },
    }

    w = board.BOARD_WIDTH
    h = board.BOARD_HEIGHT

    top = "┏" + "┳".join(_H_SEG for _ in range(w)) + "┓"
    mid = "┣" + "╋".join(_H_SEG for _ in range(w)) + "┫"
    bottom = "┗" + "┻".join(_H_SEG for _ in range(w)) + "┛"

    lines = [top]
    for row in range(h):
        cells = []
        for col in range(w):
            piece = board.get_piece(row, col)
            if piece is None:
                cells.append(_EMPTY_CELL)
            else:
                p_type, p_color = piece
                char = unicode_map.get(p_color, {}).get(p_type, "?")
                cells.append(f" {char} ")
        lines.append("┃" + "┃".join(cells) + "┃")
        if row < h - 1:
            lines.append(mid)
    lines.append(bottom)
    return "\n".join(lines)


def save_board(text: str, path: str | Path) -> None:
    """Write ``text`` representing a board to ``path``."""
    Path(path).write_text(text)
