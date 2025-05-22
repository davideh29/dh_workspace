from dh_workspace import (
    Bishop,
    Chessboard,
    King,
    Knight,
    Match,
    Pawn,
    PieceColor,
    PieceType,
    Queen,
    Rook,
)
from dh_workspace.core.backend.chessboard import Piece


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


def test_starting_position_move_counts() -> None:
    board = Chessboard()
    board.reset_board()

    piece_classes = {
        PieceType.PAWN: Pawn,
        PieceType.KNIGHT: Knight,
        PieceType.BISHOP: Bishop,
        PieceType.ROOK: Rook,
        PieceType.QUEEN: Queen,
        PieceType.KING: King,
    }

    expected_counts = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 2,
        PieceType.BISHOP: 0,
        PieceType.ROOK: 0,
        PieceType.QUEEN: 0,
        PieceType.KING: 0,
    }

    for row in range(board.BOARD_HEIGHT):
        for col in range(board.BOARD_WIDTH):
            piece_info = board.get_piece(row, col)
            if piece_info is None:
                continue
            piece_type, color = piece_info
            piece_obj = piece_classes[piece_type](color, board)
            moves = piece_obj.possible_moves(row, col)
            assert len(moves) == expected_counts[piece_type]
