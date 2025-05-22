from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from .chessboard import Chessboard, Piece
from .pieces import (
    Bishop,
    Knight,
    Pawn,
    Queen,
    Rook,
    PieceType,
)


@dataclass
class Match:
    """Track the state of a chess match."""

    board: Chessboard
    num_players: int
    current_turn: int = 0
    move_number: int = 1
    captured: List[List[Piece]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.captured = [[] for _ in range(self.num_players)]

    def next_turn(self) -> None:
        """Advance the match to the next player's turn."""
        self.current_turn = (self.current_turn + 1) % self.num_players
        self.move_number += 1

    def capture_piece(self, player_index: int, piece: Piece) -> None:
        """Record that ``piece`` was captured by ``player_index``."""
        if not 0 <= player_index < self.num_players:
            raise ValueError("Invalid player index")
        self.captured[player_index].append(piece)

    def attempt_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Attempt to move a piece and update match state."""
        piece_info = self.board.get_piece(*start)
        if piece_info is None:
            return False

        piece_type, color = piece_info
        piece_map = {
            PieceType.PAWN: Pawn,
            PieceType.KNIGHT: Knight,
            PieceType.BISHOP: Bishop,
            PieceType.ROOK: Rook,
            PieceType.QUEEN: Queen,
        }
        piece_cls = piece_map.get(piece_type)
        if piece_cls is None:
            return False

        piece_obj = piece_cls(color, self.board)
        moves = piece_obj.possible_moves(*start)
        move = next((m for m in moves if m.end == end), None)
        if move is None:
            return False

        for capture in move.captures:
            captured = self.board.get_piece(*capture)
            if captured is not None:
                self.capture_piece(self.current_turn, Piece(*captured))
                self.board.remove_piece(*capture)

        self.board.remove_piece(*start)
        self.board.place_piece(end[0], end[1], piece_type, color)
        self.next_turn()
        return True
