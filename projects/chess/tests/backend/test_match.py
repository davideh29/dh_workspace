from projects.chess import Chessboard, Match, PieceColor, PieceType
from projects.chess.core.backend.chessboard import Piece


def test_match_initial_state():
    match = Match(Chessboard(), num_players=3)
    assert match.move_number == 1
    assert match.current_turn == 0
    assert len(match.captured) == 3
    assert all(len(c) == 0 for c in match.captured)


def test_match_turn_and_capture():
    match = Match(Chessboard(), num_players=2)
    piece = Piece(PieceType.PAWN, PieceColor.WHITE)
    match.capture_piece(0, piece)
    match.next_turn()
    assert match.current_turn == 1
    assert match.move_number == 2
    assert match.captured[0][0] == piece


def test_attempt_move_success_and_fail() -> None:
    board = Chessboard()
    board.place_piece(6, 0, PieceType.PAWN, PieceColor.WHITE)
    match = Match(board, num_players=2)

    assert match.attempt_move((6, 0), (5, 0))
    assert board.get_piece(5, 0) == (PieceType.PAWN, PieceColor.WHITE)
    assert match.current_turn == 1
    assert match.move_number == 2

    assert not match.attempt_move((6, 1), (5, 1))
    assert match.current_turn == 1
    assert match.move_number == 2
