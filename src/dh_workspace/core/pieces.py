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
            if not self._is_valid(new_row, new_col):
                continue

            piece = self.board.get_piece(new_row, new_col)
            if piece is None:
                logger.debug(
                    "Knight move valid from (%s, %s) to (%s, %s)",
                    row,
                    col,
                    new_row,
                    new_col,
                )
                moves.append(PieceMove(start=(row, col), end=(new_row, new_col)))
            elif piece[1] != self.color:
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


@dataclass
class Pawn(ChessPiece):
    """Concrete ``ChessPiece`` representing a pawn."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        direction = -1 if self.color == PieceColor.WHITE else 1
        target_row = row + direction
        candidate_moves = [(0, False), (-1, True), (1, True)]
        moves: List[PieceMove] = []

        for delta_col, is_capture in candidate_moves:
            new_col = col + delta_col
            if not self._is_valid(target_row, new_col):
                continue

            piece = self.board.get_piece(target_row, new_col)
            if is_capture:
                if piece is not None and piece[1] != self.color:
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


@dataclass
class Bishop(ChessPiece):
    """Concrete ``ChessPiece`` representing a bishop."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        moves: List[PieceMove] = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for delta_row, delta_col in directions:
            step = 1
            while True:
                new_row = row + delta_row * step
                new_col = col + delta_col * step
                if not self._is_valid(new_row, new_col):
                    break

                piece = self.board.get_piece(new_row, new_col)
                if piece is None:
                    moves.append(PieceMove(start=(row, col), end=(new_row, new_col)))
                else:
                    if piece[1] != self.color:
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
