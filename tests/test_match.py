from dh_workspace import Chessboard, Match, PieceColor
from dh_workspace.chessboard import Piece


def test_match_initial_state():
    match = Match(Chessboard(), num_players=3)
    assert match.move_number == 1
    assert match.current_turn == 0
    assert len(match.captured) == 3
    assert all(len(c) == 0 for c in match.captured)


def test_match_turn_and_capture():
    match = Match(Chessboard(), num_players=2)
    piece = Piece("pawn", PieceColor.WHITE)
    match.capture_piece(0, piece)
    match.next_turn()
    assert match.current_turn == 1
    assert match.move_number == 2
    assert match.captured[0][0] == piece
