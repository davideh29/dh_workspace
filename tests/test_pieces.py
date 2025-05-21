import pytest

from dh_workspace import ChessPiece, Knight


def test_chesspiece_is_abstract() -> None:
    with pytest.raises(TypeError):
        ChessPiece("white")


def test_knight_moves_center() -> None:
    knight = Knight("white")
    moves = knight.possible_moves(4, 4)
    assert len(moves) == 8
    assert (6, 5) in moves
    assert (2, 3) in moves


def test_knight_moves_edge() -> None:
    knight = Knight("black")
    moves = knight.possible_moves(0, 0)
    assert sorted(moves) == [(1, 2), (2, 1)]
