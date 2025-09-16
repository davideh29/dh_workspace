from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from .chessboard import Chessboard, Piece
from .pieces import (
    Bishop,
    Knight,
    Pawn,
    Queen,
    Rook,
    King,
    PieceType,
    PieceColor,
)


@dataclass
class Match:
    """Track the state of a chess match."""

    board: Chessboard
    num_players: int
    current_turn: int = 0
    move_number: int = 1
    captured: List[List[Piece]] = field(default_factory=list)
    is_completed: bool = False

    _color_order = [
        PieceColor.WHITE,
        PieceColor.BLACK,
        PieceColor.RED,
        PieceColor.BLUE,
    ]

    def __post_init__(self) -> None:
        self.captured = [[] for _ in range(self.num_players)]

    def _player_color(self, index: int) -> PieceColor:
        """Return the color associated with ``index``."""
        return self._color_order[index % len(self._color_order)]

    def _find_king(self, color: PieceColor) -> Optional[Tuple[int, int]]:
        for r in range(self.board.BOARD_HEIGHT):
            for c in range(self.board.BOARD_WIDTH):
                if self.board.get_piece(r, c) == (PieceType.KING, color):
                    return r, c
        return None

    def _is_in_check(self, color: PieceColor) -> bool:
        from .moves import _square_under_attack

        pos = self._find_king(color)
        if pos is None:
            return False
        return _square_under_attack(self.board, color, pos[0], pos[1])

    def _has_escape_moves(self, color: PieceColor) -> bool:
        from .moves import generate_moves

        if self._find_king(color) is None:
            return False

        for r in range(self.board.BOARD_HEIGHT):
            for c in range(self.board.BOARD_WIDTH):
                piece = self.board.get_piece(r, c)
                if piece is None:
                    continue
                piece_type, p_color = piece
                if p_color != color:
                    continue
                moves = generate_moves(piece_type, self.board, p_color, r, c)
                for m in moves:
                    board_copy = self.board.clone()
                    for cap in m.captures:
                        board_copy.remove_piece(*cap)
                    board_copy.remove_piece(r, c)
                    board_copy.place_piece(m.end[0], m.end[1], piece_type, p_color)
                    new_pos = (
                        m.end
                        if piece_type == PieceType.KING
                        else self._find_king(color)
                    )
                    if new_pos is None:
                        continue
                    from .moves import _square_under_attack

                    if not _square_under_attack(
                        board_copy, color, new_pos[0], new_pos[1]
                    ):
                        return True
        return False

    def _is_checkmate(self, color: PieceColor) -> bool:
        return self._is_in_check(color) and not self._has_escape_moves(color)

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
        if self.is_completed:
            return False
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
            PieceType.KING: King,
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
            if captured is not None and captured[0] == PieceType.KING:
                return False

        for capture in move.captures:
            captured = self.board.get_piece(*capture)
            if captured is not None:
                self.capture_piece(self.current_turn, Piece(*captured))
                self.board.remove_piece(*capture)

        self.board.remove_piece(*start)
        self.board.place_piece(end[0], end[1], piece_type, color)
        opponent_index = (self.current_turn + 1) % self.num_players
        if self._is_checkmate(self._player_color(opponent_index)):
            self.is_completed = True
        else:
            self.next_turn()
        return True
