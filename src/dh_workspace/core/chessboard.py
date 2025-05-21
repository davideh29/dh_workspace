from dataclasses import dataclass
from typing import Optional, Tuple

from ..utils.config import CONFIG
from ..utils.logger import logger
from .pieces import PieceColor


@dataclass
class Piece:
    """Represents a chess piece and its color."""

    piece: str
    color: PieceColor


class Chessboard:
    """Class representing state of a chessboard."""

    def __init__(self) -> None:
        """Initialize an empty chessboard."""
        self.BOARD_SIZE = CONFIG.board_size
        logger.debug("Initializing chessboard with size %s", self.BOARD_SIZE)
        self._board: list[list[Optional[Piece]]] = [
            [None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]

    def _validate_position(self, row: int, col: int) -> None:
        """Raise ``ValueError`` if ``row`` or ``col`` is outside the board."""
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            raise ValueError("Position out of bounds")

    def place_piece(self, row: int, col: int, piece: str, color: PieceColor) -> None:
        """Place a piece at the given position."""
        self._validate_position(row, col)
        self._board[row][col] = Piece(piece, color)

    def remove_piece(self, row: int, col: int) -> None:
        """Remove any piece from the given position."""
        self._validate_position(row, col)
        self._board[row][col] = None

    def get_piece(self, row: int, col: int) -> Optional[Tuple[str, PieceColor]]:
        """Return the piece and color at the given position, or ``None`` if empty."""
        self._validate_position(row, col)
        data = self._board[row][col]
        if data is None:
            return None
        return data.piece, data.color

    def is_empty(self, row: int, col: int) -> bool:
        """Return ``True`` if the square is empty."""
        self._validate_position(row, col)
        return self._board[row][col] is None
