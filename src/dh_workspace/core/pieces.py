from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple


@dataclass
class PieceMove:
    """Represents a potential move for a piece."""

    start: Tuple[int, int]
    end: Tuple[int, int]
    captures: List[Tuple[int, int]] = field(default_factory=list)


from typing import TYPE_CHECKING

from ..utils.config import CONFIG
from ..utils.logger import logger

if TYPE_CHECKING:  # pragma: no cover - only for type hints
    from .chessboard import Chessboard


class PieceColor(Enum):
    """Enumeration of chess piece colors."""

    WHITE = "white"
    BLACK = "black"
    RED = "red"
    BLUE = "blue"


class PieceType(Enum):
    """Enumeration of chess piece identifiers."""

    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"


def _is_valid(board: "Chessboard", row: int, col: int) -> bool:
    """Return ``True`` if the position is on ``board``."""
    return 0 <= row < board.BOARD_HEIGHT and 0 <= col < board.BOARD_WIDTH


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


@dataclass
class ChessPiece(ABC):
    """Base class for chess pieces."""

    color: PieceColor
    board: "Chessboard"

    @abstractmethod
    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        """Return a list of possible moves from ``row`` and ``col``."""

    def _is_valid(self, row: int, col: int) -> bool:
        """Return ``True`` if the position is on the board."""
        width = CONFIG.board_width
        height = CONFIG.board_height
        return 0 <= row < height and 0 <= col < width


@dataclass
class Knight(ChessPiece):
    """Concrete ``ChessPiece`` representing a knight."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_knight_moves(self.board, self.color, row, col)


@dataclass
class Pawn(ChessPiece):
    """Concrete ``ChessPiece`` representing a pawn."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_pawn_moves(self.board, self.color, row, col)


@dataclass
class Bishop(ChessPiece):
    """Concrete ``ChessPiece`` representing a bishop."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_bishop_moves(self.board, self.color, row, col)


@dataclass
class Rook(ChessPiece):
    """Concrete ``ChessPiece`` representing a rook."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_rook_moves(self.board, self.color, row, col)


@dataclass
class Queen(ChessPiece):
    """Concrete ``ChessPiece`` representing a queen."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_queen_moves(self.board, self.color, row, col)
