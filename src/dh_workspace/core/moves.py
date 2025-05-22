from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from .pieces import PieceMove, PieceColor, PieceType
from ..utils.logger import logger

if TYPE_CHECKING:  # pragma: no cover - only for type hints
    from .chessboard import Chessboard


def _is_valid(board: "Chessboard", row: int, col: int) -> bool:
    """Return ``True`` if the position is on ``board``."""
    return 0 <= row < board.BOARD_HEIGHT and 0 <= col < board.BOARD_WIDTH


def _square_under_attack(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> bool:
    """Return ``True`` if ``row`` and ``col`` are threatened by any enemy piece."""
    for r in range(board.BOARD_HEIGHT):
        for c in range(board.BOARD_WIDTH):
            piece = board.get_piece(r, c)
            if piece is None:
                continue
            piece_type, piece_color = piece
            if piece_color == color:
                continue
            if piece_type == PieceType.KNIGHT:
                moves = generate_knight_moves(board, piece_color, r, c)
            elif piece_type == PieceType.PAWN:
                moves = generate_pawn_moves(board, piece_color, r, c)
            elif piece_type == PieceType.BISHOP:
                moves = generate_bishop_moves(board, piece_color, r, c)
            elif piece_type == PieceType.ROOK:
                moves = generate_rook_moves(board, piece_color, r, c)
            elif piece_type == PieceType.QUEEN:
                moves = generate_queen_moves(board, piece_color, r, c)
            elif piece_type == PieceType.KING:
                moves = generate_king_moves(board, piece_color, r, c, safe_moves=False)
            else:
                continue
            for move in moves:
                if move.end == (row, col):
                    return True
    return False


def generate_knight_moves(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> List[PieceMove]:
    """Return all legal knight moves from ``row`` and ``col``."""
    deltas = [
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    ]
    moves: List[PieceMove] = []
    for delta_row, delta_col in deltas:
        new_row = row + delta_row
        new_col = col + delta_col
        if not _is_valid(board, new_row, new_col):
            continue

        piece = board.get_piece(new_row, new_col)
        if piece is None:
            logger.debug(
                "Knight move valid from (%s, %s) to (%s, %s)",
                row,
                col,
                new_row,
                new_col,
            )
            moves.append(PieceMove(start=(row, col), end=(new_row, new_col)))
        elif piece[1] != color:
            logger.debug(
                "Knight capture from (%s, %s) to (%s, %s)",
                row,
                col,
                new_row,
                new_col,
            )
            moves.append(
                PieceMove(
                    start=(row, col),
                    end=(new_row, new_col),
                    captures=[(new_row, new_col)],
                )
            )
    return moves


def generate_pawn_moves(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> List[PieceMove]:
    """Return all legal pawn moves from ``row`` and ``col``."""
    direction = -1 if color == PieceColor.WHITE else 1
    target_row = row + direction
    candidate_moves = [(0, False), (-1, True), (1, True)]
    moves: List[PieceMove] = []

    for delta_col, is_capture in candidate_moves:
        new_col = col + delta_col
        if not _is_valid(board, target_row, new_col):
            continue

        piece = board.get_piece(target_row, new_col)
        if is_capture:
            if piece is not None and piece[1] != color:
                logger.debug(
                    "Pawn capture from (%s, %s) to (%s, %s)",
                    row,
                    col,
                    target_row,
                    new_col,
                )
                moves.append(
                    PieceMove(
                        start=(row, col),
                        end=(target_row, new_col),
                        captures=[(target_row, new_col)],
                    )
                )
        else:
            if piece is None:
                logger.debug(
                    "Pawn move valid from (%s, %s) to (%s, %s)",
                    row,
                    col,
                    target_row,
                    new_col,
                )
                moves.append(PieceMove(start=(row, col), end=(target_row, new_col)))
    return moves


def generate_bishop_moves(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> List[PieceMove]:
    """Return all legal bishop moves from ``row`` and ``col``."""
    moves: List[PieceMove] = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for delta_row, delta_col in directions:
        step = 1
        while True:
            new_row = row + delta_row * step
            new_col = col + delta_col * step
            if not _is_valid(board, new_row, new_col):
                break

            piece = board.get_piece(new_row, new_col)
            if piece is None:
                moves.append(PieceMove(start=(row, col), end=(new_row, new_col)))
            else:
                if piece[1] != color:
                    moves.append(
                        PieceMove(
                            start=(row, col),
                            end=(new_row, new_col),
                            captures=[(new_row, new_col)],
                        )
                    )
                break
            step += 1
    return moves


def generate_rook_moves(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> List[PieceMove]:
    """Return all legal rook moves from ``row`` and ``col``."""
    moves: List[PieceMove] = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for delta_row, delta_col in directions:
        step = 1
        while True:
            new_row = row + delta_row * step
            new_col = col + delta_col * step
            if not _is_valid(board, new_row, new_col):
                break

            piece = board.get_piece(new_row, new_col)
            if piece is None:
                moves.append(PieceMove(start=(row, col), end=(new_row, new_col)))
            else:
                if piece[1] != color:
                    moves.append(
                        PieceMove(
                            start=(row, col),
                            end=(new_row, new_col),
                            captures=[(new_row, new_col)],
                        )
                    )
                break
            step += 1
    return moves


def generate_queen_moves(
    board: "Chessboard", color: PieceColor, row: int, col: int
) -> List[PieceMove]:
    """Return all legal queen moves from ``row`` and ``col``."""
    return generate_rook_moves(board, color, row, col) + generate_bishop_moves(
        board, color, row, col
    )


def generate_king_moves(
    board: "Chessboard",
    color: PieceColor,
    row: int,
    col: int,
    safe_moves: bool = True,
) -> List[PieceMove]:
    """Return all legal king moves from ``row`` and ``col``."""
    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    moves: List[PieceMove] = []
    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col
        if not _is_valid(board, new_row, new_col):
            continue
        piece = board.get_piece(new_row, new_col)
        if piece is None or piece[1] != color:
            if safe_moves:
                if piece is not None and piece[1] != color:
                    board.remove_piece(new_row, new_col)
                    danger = _square_under_attack(board, color, new_row, new_col)
                    board.place_piece(new_row, new_col, piece[0], piece[1])
                else:
                    danger = _square_under_attack(board, color, new_row, new_col)
                if danger:
                    continue
            captures = [] if piece is None else [(new_row, new_col)]
            moves.append(
                PieceMove(start=(row, col), end=(new_row, new_col), captures=captures)
            )
    return moves


def generate_moves(
    piece: PieceType,
    board: "Chessboard",
    color: PieceColor,
    row: int,
    col: int,
) -> List[PieceMove]:
    """Return the legal moves for ``piece`` at ``row`` and ``col``."""
    if piece == PieceType.KNIGHT:
        return generate_knight_moves(board, color, row, col)
    if piece == PieceType.PAWN:
        return generate_pawn_moves(board, color, row, col)
    if piece == PieceType.BISHOP:
        return generate_bishop_moves(board, color, row, col)
    if piece == PieceType.ROOK:
        return generate_rook_moves(board, color, row, col)
    if piece == PieceType.QUEEN:
        return generate_queen_moves(board, color, row, col)
    if piece == PieceType.KING:
        return generate_king_moves(board, color, row, col)
    raise ValueError(f"Unsupported piece type: {piece}")
