from pathlib import Path

from projects.chess import (
    Chessboard,
    Match,
    CONFIG,
    draw_board,
    draw_board_inverted,
    draw_empty_board,
    save_board,
)


def test_draw_empty_board_saves_file() -> None:
    """Ensure drawing the empty board matches the stored resource."""
    board = draw_empty_board()
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "empty_board.txt"
    if not output_file.exists():
        save_board(board, output_file)
    assert output_file.read_text() == board


def test_draw_starting_board_saves_file() -> None:
    """Ensure drawing the starting board matches the stored resource."""
    chessboard = Chessboard()
    chessboard.reset_board()
    board_text = draw_board(chessboard)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "starting_board.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_draw_starting_board_with_coords() -> None:
    """Ensure drawing the numbered starting board matches the stored resource."""

    chessboard = Chessboard()
    chessboard.reset_board()
    board_text = draw_board(chessboard, with_coords=True)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "starting_board_coords.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_unicode_board_structure() -> None:
    """Verify that ``draw_empty_board`` uses box drawing characters."""

    expected = "┏━━━┳━━━┓\n" "┃   ┃   ┃\n" "┣━━━╋━━━┫\n" "┃   ┃   ┃\n" "┗━━━┻━━━┛\n"
    assert draw_empty_board(width=2, height=2) == expected


def test_board_after_pawn_and_knight_moves() -> None:
    """Regression test for board state after pawn and knight moves."""
    board = Chessboard()
    board.reset_board()
    match = Match(board, num_players=2)

    assert match.attempt_move((6, 0), (5, 0))
    assert match.attempt_move((1, 0), (2, 0))
    assert match.attempt_move((7, 1), (5, 2))
    assert match.attempt_move((0, 1), (2, 2))

    board_text = draw_board(board)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "pawn_knight_moves.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_draw_empty_board_with_coords() -> None:
    """Ensure coordinates are added when requested."""

    expected = (
        "  ┏━━━┳━━━┓\n"
        "2 ┃   ┃   ┃\n"
        "  ┣━━━╋━━━┫\n"
        "1 ┃   ┃   ┃\n"
        "  ┗━━━┻━━━┛\n"
        "   A   B\n"
    )
    assert draw_empty_board(width=2, height=2, with_coords=True) == expected


def test_draw_board_inverted() -> None:
    """The inverted board should show white pieces at the top."""

    board = Chessboard()
    board.reset_board()
    top_row = draw_board_inverted(board).splitlines()[1]
    assert "♖" in top_row
    assert "♜" not in top_row


def test_draw_starting_board_inverted_saves_file() -> None:
    """Regression test for the full inverted starting board."""

    board = Chessboard()
    board.reset_board()
    board_text = draw_board_inverted(board)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "inverted_starting_board.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_draw_starting_board_inverted_with_coords() -> None:
    """Regression test for inverted starting board with coordinates."""

    board = Chessboard()
    board.reset_board()
    board_text = draw_board_inverted(board, with_coords=True)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "inverted_starting_board_coords.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_inverted_board_after_several_moves() -> None:
    """Regression test for an inverted board after multiple moves."""

    board = Chessboard()
    board.reset_board()
    match = Match(board, num_players=2)

    moves = [
        ((6, 4), (5, 4)),
        ((1, 3), (2, 3)),
        ((6, 0), (5, 0)),
        ((1, 0), (2, 0)),
        ((7, 1), (5, 2)),
        ((0, 1), (2, 2)),
        ((7, 6), (5, 5)),
        ((0, 6), (2, 5)),
    ]

    for start, end in moves:
        assert match.attempt_move(start, end)

    board_text = draw_board_inverted(board, with_coords=True)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "inverted_moves.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_draw_non_standard_size_board() -> None:
    """Regression test for drawing a smaller board."""

    old_w, old_h = CONFIG.board_width, CONFIG.board_height
    CONFIG.board_width = 5
    CONFIG.board_height = 4
    try:
        board = Chessboard()
        board.reset_board()
        board_text = draw_board(board, with_coords=True)
    finally:
        CONFIG.board_width = old_w
        CONFIG.board_height = old_h

    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "non_standard_board.txt"
    if not output_file.exists():
        save_board(board_text, output_file)
    assert output_file.read_text() == board_text
