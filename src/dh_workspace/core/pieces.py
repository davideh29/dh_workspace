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


from ..utils.config import CONFIG
from ..utils.logger import logger


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
        for dr, dc in deltas:
            new_row = row + dr
            new_col = col + dc
            if self._is_valid(new_row, new_col):
                logger.debug(
                    "Knight move valid from (%s, %s) to (%s, %s)",
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
        new_row = row + direction
        moves: List[PieceMove] = []
        if self._is_valid(new_row, col):
            logger.debug(
                "Pawn move valid from (%s, %s) to (%s, %s)",
                row,
                col,
                new_row,
                col,
            )
            moves.append(PieceMove(start=(row, col), end=(new_row, col)))
        for dc in (-1, 1):
            new_col = col + dc
            if self._is_valid(new_row, new_col):
                logger.debug(
                    "Pawn capture from (%s, %s) to (%s, %s)",
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
