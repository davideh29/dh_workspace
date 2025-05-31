from dh_workspace import MatchFacade, PieceType, PieceColor


def test_facade_initial_state_and_move():
    facade = MatchFacade(num_players=2)
    assert facade.get_current_turn() == 0
    assert facade.get_move_number() == 1

    moves = facade.get_valid_moves(6, 0)
    assert (5, 0) in {m.end for m in moves}

    assert facade.move_piece((6, 0), (5, 0))
    assert facade.board.get_piece(5, 0) == (PieceType.PAWN, PieceColor.WHITE)
    assert facade.get_current_turn() == 1
    assert facade.get_move_number() == 2


def test_facade_reset_game():
    facade = MatchFacade(num_players=2)
    facade.move_piece((6, 0), (5, 0))
    assert facade.get_current_turn() == 1

    facade.reset_game()
    assert facade.board.get_piece(6, 0) == (PieceType.PAWN, PieceColor.WHITE)
    assert facade.get_current_turn() == 0
    assert facade.get_move_number() == 1


def test_facade_get_valid_moves_empty_square():
    facade = MatchFacade(num_players=2)
    assert facade.get_valid_moves(3, 3) == []
