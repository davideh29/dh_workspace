from __future__ import annotations

"""High level API for interacting with a chess match."""

from typing import List, Tuple

from .backend.chessboard import Chessboard
from .backend.match import Match
from .backend.pieces import (
    Bishop,
    King,
    Knight,
    Pawn,
    Queen,
    Rook,
    PieceType,
    PieceMove,
)


class MatchFacade:
    """Simple facade exposing high level game operations."""

    def __init__(self, num_players: int = 2) -> None:
        self._num_players = num_players
        self.reset_game()

    def reset_game(self) -> None:
        """Reset the board and match to the starting position."""
        self.board = Chessboard()
        self.board.reset_board()
        self.match = Match(self.board, num_players=self._num_players)

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Move a piece from ``start`` to ``end`` if the move is legal."""
        return self.match.attempt_move(start, end)

    def get_valid_moves(self, row: int, col: int) -> List[PieceMove]:
        """Return all legal moves for the piece at ``row`` and ``col``."""
        piece_info = self.board.get_piece(row, col)
        if piece_info is None:
            return []

        piece_type, color = piece_info
        piece_map = {
            PieceType.PAWN: Pawn,
            PieceType.KNIGHT: Knight,
            PieceType.BISHOP: Bishop,
            PieceType.ROOK: Rook,
            PieceType.QUEEN: Queen,
            PieceType.KING: King,
        }
        piece_cls = piece_map[piece_type]
        piece_obj = piece_cls(color, self.board)
        return piece_obj.possible_moves(row, col)

    def get_current_turn(self) -> int:
        """Return the index of the player whose turn it is."""
        return self.match.current_turn

    def get_move_number(self) -> int:
        """Return the overall move number in the match."""
        return self.match.move_number
