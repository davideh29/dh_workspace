import pytest

from dh_workspace import (
    ChessPiece,
    Chessboard,
    Knight,
    Pawn,
    Bishop,
    Rook,
    PieceColor,
)


def test_chesspiece_is_abstract() -> None:
    board = Chessboard()
    with pytest.raises(TypeError):
        ChessPiece(PieceColor.WHITE, board)  # type: ignore


def test_knight_moves_center() -> None:
    board = Chessboard()
    knight = Knight(PieceColor.WHITE, board)
    moves = knight.possible_moves(4, 4)
    assert len(moves) == 8
    ends = {m.end for m in moves}
    assert (6, 5) in ends
    assert (2, 3) in ends


def test_knight_capture() -> None:
    board = Chessboard()
    knight = Knight(PieceColor.WHITE, board)
    board.place_piece(5, 6, "pawn", PieceColor.BLACK)
    board.place_piece(6, 5, "pawn", PieceColor.WHITE)
    moves = knight.possible_moves(4, 4)
    ends = {m.end for m in moves}
    assert (6, 5) not in ends
    assert (5, 6) in ends
    capture = [m for m in moves if m.end == (5, 6)][0]
    assert capture.captures == [(5, 6)]


def test_pawn_moves_forward() -> None:
    board = Chessboard()
    pawn = Pawn(PieceColor.WHITE, board)
    moves = pawn.possible_moves(4, 4)
    assert [(3, 4)] == [m.end for m in moves]


def test_pawn_capture() -> None:
    board = Chessboard()
    pawn = Pawn(PieceColor.WHITE, board)
    board.place_piece(3, 3, "pawn", PieceColor.BLACK)
    moves = pawn.possible_moves(4, 4)
    ends = {m.end for m in moves}
    assert (3, 4) in ends
    assert (3, 3) in ends
    capture = [m for m in moves if m.end == (3, 3)][0]
    assert capture.captures == [(3, 3)]


def test_pawn_blocked() -> None:
    board = Chessboard()
    pawn = Pawn(PieceColor.WHITE, board)
    board.place_piece(3, 4, "pawn", PieceColor.WHITE)
    moves = pawn.possible_moves(4, 4)
    assert moves == []


def test_bishop_moves_diagonally() -> None:
    board = Chessboard()
    bishop = Bishop(PieceColor.WHITE, board)
    moves = bishop.possible_moves(4, 4)
    assert len(moves) == 13
    ends = {m.end for m in moves}
    assert (0, 0) in ends
    assert (7, 7) in ends
    assert (3, 5) in ends


def test_bishop_capture_and_block() -> None:
    board = Chessboard()
    bishop = Bishop(PieceColor.WHITE, board)
    board.place_piece(6, 6, "pawn", PieceColor.BLACK)
    board.place_piece(2, 2, "pawn", PieceColor.WHITE)
    moves = bishop.possible_moves(4, 4)
    ends = {m.end for m in moves}
    assert (6, 6) in ends
    assert (7, 7) not in ends
    assert (2, 2) not in ends


def test_rook_moves_straight() -> None:
    board = Chessboard()
    rook = Rook(PieceColor.WHITE, board)
    moves = rook.possible_moves(4, 4)
    assert len(moves) == 14
    ends = {m.end for m in moves}
    assert (0, 4) in ends
    assert (7, 4) in ends
    assert (4, 0) in ends
    assert (4, 7) in ends


def test_rook_capture_and_block() -> None:
    board = Chessboard()
    rook = Rook(PieceColor.WHITE, board)
    board.place_piece(4, 6, "pawn", PieceColor.BLACK)
    board.place_piece(1, 4, "pawn", PieceColor.BLACK)
    board.place_piece(4, 2, "pawn", PieceColor.WHITE)
    moves = rook.possible_moves(4, 4)
    ends = {m.end for m in moves}
    assert (4, 6) in ends
    assert (1, 4) in ends
    assert (4, 7) not in ends
    assert (0, 4) not in ends
    assert (4, 2) not in ends
    assert (4, 1) not in ends
    capture1 = [m for m in moves if m.end == (4, 6)][0]
    capture2 = [m for m in moves if m.end == (1, 4)][0]
    assert capture1.captures == [(4, 6)]
    assert capture2.captures == [(1, 4)]
