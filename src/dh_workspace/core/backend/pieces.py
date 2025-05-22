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

from ...utils.config import CONFIG


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
    KING = "king"


from .moves import generate_moves


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
        return generate_moves(PieceType.KNIGHT, self.board, self.color, row, col)


@dataclass
class Pawn(ChessPiece):
    """Concrete ``ChessPiece`` representing a pawn."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_moves(PieceType.PAWN, self.board, self.color, row, col)


@dataclass
class Bishop(ChessPiece):
    """Concrete ``ChessPiece`` representing a bishop."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_moves(PieceType.BISHOP, self.board, self.color, row, col)


@dataclass
class Rook(ChessPiece):
    """Concrete ``ChessPiece`` representing a rook."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_moves(PieceType.ROOK, self.board, self.color, row, col)


@dataclass
class Queen(ChessPiece):
    """Concrete ``ChessPiece`` representing a queen."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_moves(PieceType.QUEEN, self.board, self.color, row, col)


@dataclass
class King(ChessPiece):
    """Concrete ``ChessPiece`` representing a king."""

    def possible_moves(self, row: int, col: int) -> List[PieceMove]:
        return generate_moves(PieceType.KING, self.board, self.color, row, col)
