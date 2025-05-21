from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .chessboard import Chessboard, Piece


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
