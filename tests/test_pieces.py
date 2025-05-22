import pytest

from dh_workspace import ChessPiece, Knight, Pawn, PieceMove, PieceColor


def test_chesspiece_is_abstract() -> None:
    with pytest.raises(TypeError):
        ChessPiece(PieceColor.WHITE)  # type: ignore


def test_knight_moves_center() -> None:
    knight = Knight(PieceColor.WHITE)
    moves = knight.possible_moves(4, 4)
    assert len(moves) == 8
    ends = [m.end for m in moves]
    assert (6, 5) in ends
    assert (2, 3) in ends


def test_knight_moves_edge() -> None:
    knight = Knight(PieceColor.BLACK)
    moves = knight.possible_moves(0, 0)
    assert len(moves) == 8
    ends = {m.end for m in moves}
    assert (1, 2) in ends
    assert (-1, -2) in ends


def test_pawn_moves() -> None:
    pawn = Pawn(PieceColor.WHITE)
    moves = pawn.possible_moves(4, 4)
    ends = {m.end for m in moves}
    assert (3, 4) in ends
    assert (3, 3) in ends
    assert (3, 5) in ends
