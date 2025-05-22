"""ASCII chessboard drawing utilities."""

from __future__ import annotations

from pathlib import Path

from ..utils.config import CONFIG


def draw_empty_board(width: int | None = None, height: int | None = None) -> str:
    """Return a simple ASCII representation of an empty chessboard."""
    w = width or CONFIG.board_width
    h = height or CONFIG.board_height

    # The top border should align with the left edge of the board
    # so we avoid introducing a leading space.
    top_border = "_" + " _" * (w - 1)
    lines = [top_border]
    for _ in range(h):
        line = "|" + "_|" * w
        lines.append(line)
    return "\n".join(lines)


def draw_board(board: "Chessboard") -> str:
    """Return a Unicode representation of ``board``."""
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
    lines = ["_" + " _" * (w - 1)]
    for row in range(h):
        cells = []
        for col in range(w):
            piece = board.get_piece(row, col)
            if piece is None:
                cells.append("_")
                continue
            p_type, p_color = piece
            char = unicode_map.get(p_color, {}).get(p_type, "?")
            cells.append(char)
        line = "|" + "|".join(cells) + "|"
        lines.append(line)
    return "\n".join(lines)


def save_board(text: str, path: str | Path) -> None:
    """Write ``text`` representing a board to ``path``."""
    Path(path).write_text(text)
