"""Unicode chessboard drawing utilities."""

from __future__ import annotations

from pathlib import Path

from ..utils.config import CONFIG


_H_SEG = "━" * 3
_EMPTY_CELL = " " * 3


def draw_empty_board(
    width: int | None = None,
    height: int | None = None,
    *,
    with_coords: bool = False,
) -> str:
    """Return a Unicode board with empty squares.

    Parameters
    ----------
    width:
        Optional board width. Defaults to ``CONFIG.board_width``.
    height:
        Optional board height. Defaults to ``CONFIG.board_height``.
    with_coords:
        If ``True``, include numeric coordinates along the left and bottom
        edges of the board.
    """

    w = width or CONFIG.board_width
    h = height or CONFIG.board_height

    top = "┏" + "┳".join(_H_SEG for _ in range(w)) + "┓"
    mid = "┣" + "╋".join(_H_SEG for _ in range(w)) + "┫"
    bottom = "┗" + "┻".join(_H_SEG for _ in range(w)) + "┛"

    lines: list[str] = [top if not with_coords else f"  {top}"]
    for row in range(h):
        row_line = "┃" + "┃".join(_EMPTY_CELL for _ in range(w)) + "┃"
        if with_coords:
            lines.append(f"{row + 1} {row_line}")
        else:
            lines.append(row_line)
        if row < h - 1:
            lines.append(mid if not with_coords else f"  {mid}")
    lines.append(bottom if not with_coords else f"  {bottom}")
    if with_coords:
        lines.append("  " + "   ".join(str(i + 1) for i in range(w)))
    return "\n".join(lines) + "\n"


def draw_board(
    board: "Chessboard", *, with_coords: bool = False, invert: bool = False
) -> str:
    """Return a Unicode chessboard containing the pieces from ``board``.

    Parameters
    ----------
    board:
        The ``Chessboard`` instance to render.
    with_coords:
        If ``True``, include numeric coordinates along the left and bottom
        edges of the board.
    invert:
        If ``True``, draw the board upside down. Useful when switching the
        player's perspective.
    """

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

    row_range = range(h - 1, -1, -1) if invert else range(h)
    col_range = range(w - 1, -1, -1) if invert else range(w)

    lines: list[str] = [top if not with_coords else f"  {top}"]
    for idx, row in enumerate(row_range):
        cells = []
        for col in col_range:
            piece = board.get_piece(row, col)
            if piece is None:
                cells.append(_EMPTY_CELL)
            else:
                p_type, p_color = piece
                char = unicode_map.get(p_color, {}).get(p_type, "?")
                cells.append(f" {char} ")
        row_line = "┃" + "┃".join(cells) + "┃"
        if with_coords:
            lines.append(f"{idx + 1} {row_line}")
        else:
            lines.append(row_line)
        if idx < h - 1:
            lines.append(mid if not with_coords else f"  {mid}")
    lines.append(bottom if not with_coords else f"  {bottom}")
    if with_coords:
        bottom_range = range(w - 1, -1, -1) if invert else range(w)
        lines.append("  " + "   ".join(str(i + 1) for i in bottom_range))
    return "\n".join(lines) + "\n"


def draw_board_inverted(board: "Chessboard", *, with_coords: bool = False) -> str:
    """Return ``board`` drawn upside down."""

    return draw_board(board, with_coords=with_coords, invert=True)


def save_board(text: str, path: str | Path) -> None:
    """Write ``text`` representing a board to ``path``."""
    Path(path).write_text(text)
