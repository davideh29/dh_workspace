from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


BOARD_SIZE = 8


@dataclass
class ChessPiece(ABC):
    """Base class for chess pieces."""

    color: str

    @abstractmethod
    def possible_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Return a list of possible moves from ``row`` and ``col``."""

    def _is_valid(self, row: int, col: int) -> bool:
        """Return ``True`` if the position is on the board."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


@dataclass
class Knight(ChessPiece):
    """Concrete ``ChessPiece`` representing a knight."""

    def possible_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
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
        moves: List[Tuple[int, int]] = []
        for dr, dc in deltas:
            new_row = row + dr
            new_col = col + dc
            if self._is_valid(new_row, new_col):
                moves.append((new_row, new_col))
        return moves
