from dh_workspace import Chessboard, Match, PieceColor, PieceType
from dh_workspace.core.chessboard import Piece


def test_pawn_capture_sequence() -> None:
    board = Chessboard()
    board.reset_board()
    match = Match(board, num_players=2)

    assert match.attempt_move((6, 3), (5, 3))
    assert match.attempt_move((1, 4), (2, 4))
    assert match.attempt_move((5, 3), (4, 3))
    assert match.attempt_move((2, 4), (3, 4))
    assert match.attempt_move((4, 3), (3, 4))

    assert board.get_piece(3, 4) == (PieceType.PAWN, PieceColor.WHITE)
    assert len(match.captured[0]) == 1
    captured_piece = match.captured[0][0]
    assert captured_piece == Piece(PieceType.PAWN, PieceColor.BLACK)
