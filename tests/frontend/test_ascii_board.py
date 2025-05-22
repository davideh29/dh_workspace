from pathlib import Path

from dh_workspace import Chessboard, draw_board, draw_empty_board, save_board


def test_draw_empty_board_saves_file(tmp_path: Path) -> None:
    """Draw an empty board and save it to the resources directory."""
    board = draw_empty_board()
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "empty_board.txt"
    save_board(board, output_file)
    assert output_file.read_text() == board


def test_draw_starting_board_saves_file(tmp_path: Path) -> None:
    """Draw the starting board and save it to the resources directory."""
    chessboard = Chessboard()
    chessboard.reset_board()
    board_text = draw_board(chessboard)
    resources_dir = Path(__file__).parents[1] / "resources"
    resources_dir.mkdir(exist_ok=True)
    output_file = resources_dir / "starting_board.txt"
    save_board(board_text, output_file)
    assert output_file.read_text() == board_text


def test_unicode_board_structure() -> None:
    """Verify that ``draw_empty_board`` uses box drawing characters."""

    expected = "┏━━━┳━━━┓\n" "┃   ┃   ┃\n" "┣━━━╋━━━┫\n" "┃   ┃   ┃\n" "┗━━━┻━━━┛"
    assert draw_empty_board(width=2, height=2) == expected
