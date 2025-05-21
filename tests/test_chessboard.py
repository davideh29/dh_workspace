import pytest

from dh_workspace import Chessboard, PieceColor


def test_board_initially_empty():
    board = Chessboard()
    for row in range(board.BOARD_SIZE):
        for col in range(board.BOARD_SIZE):
            assert board.is_empty(row, col)
            assert board.get_piece(row, col) is None


def test_place_and_get_piece():
    board = Chessboard()
    board.place_piece(0, 0, "rook", PieceColor.WHITE)
    assert not board.is_empty(0, 0)
    assert board.get_piece(0, 0) == ("rook", PieceColor.WHITE)


def test_remove_piece():
    board = Chessboard()
    board.place_piece(1, 1, "knight", PieceColor.BLACK)
    board.remove_piece(1, 1)
    assert board.is_empty(1, 1)
    assert board.get_piece(1, 1) is None


def test_invalid_position():
    board = Chessboard()
    with pytest.raises(ValueError):
        board.place_piece(-1, 0, "bishop", PieceColor.WHITE)
    with pytest.raises(ValueError):
        board.get_piece(8, 0)
