import pytest

from dh_workspace import ChessPiece, Knight, PieceMove


def test_chesspiece_is_abstract() -> None:
    with pytest.raises(TypeError):
        ChessPiece("white")


def test_knight_moves_center() -> None:
    knight = Knight("white")
    moves = knight.possible_moves(4, 4)
    assert len(moves) == 8
    ends = [m.end for m in moves]
    assert (6, 5) in ends
    assert (2, 3) in ends


def test_knight_moves_edge() -> None:
    knight = Knight("black")
    moves = knight.possible_moves(0, 0)
    assert len(moves) == 8
    ends = {m.end for m in moves}
    assert (1, 2) in ends
    assert (-1, -2) in ends
