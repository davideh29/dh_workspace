import pytest

from projects.chess import Chessboard, PieceColor, PieceType


def test_board_initially_empty():
    board = Chessboard()
    for row in range(board.BOARD_HEIGHT):
        for col in range(board.BOARD_WIDTH):
            assert board.is_empty(row, col)
            assert board.get_piece(row, col) is None


def test_place_and_get_piece():
    board = Chessboard()
    board.place_piece(0, 0, PieceType.ROOK, PieceColor.WHITE)
    assert not board.is_empty(0, 0)
    assert board.get_piece(0, 0) == (PieceType.ROOK, PieceColor.WHITE)


def test_remove_piece():
    board = Chessboard()
    board.place_piece(1, 1, PieceType.KNIGHT, PieceColor.BLACK)
    board.remove_piece(1, 1)
    assert board.is_empty(1, 1)
    assert board.get_piece(1, 1) is None


def test_invalid_position():
    board = Chessboard()
    with pytest.raises(ValueError):
        board.place_piece(-1, 0, PieceType.BISHOP, PieceColor.WHITE)
    with pytest.raises(ValueError):
        board.get_piece(8, 0)


def test_reset_board() -> None:
    board = Chessboard()
    board.reset_board()
    assert board.get_piece(6, 0) == (PieceType.PAWN, PieceColor.WHITE)
    assert board.get_piece(1, 7) == (PieceType.PAWN, PieceColor.BLACK)
    assert board.get_piece(7, 0) == (PieceType.ROOK, PieceColor.WHITE)
    assert board.get_piece(0, 1) == (PieceType.KNIGHT, PieceColor.BLACK)
    assert board.get_piece(7, 3) == (PieceType.QUEEN, PieceColor.WHITE)
    assert board.get_piece(7, 4) == (PieceType.KING, PieceColor.WHITE)
    assert board.get_piece(0, 4) == (PieceType.KING, PieceColor.BLACK)
