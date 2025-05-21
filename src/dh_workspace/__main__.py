import argparse
import logging

from . import Chessboard, Config, configure, logger


def main() -> None:
    parser = argparse.ArgumentParser(description="dh_workspace entry point")
    parser.add_argument("--board-size", type=int, default=Config().board_size)
    parser.add_argument(
        "--log-level", default=logging.getLevelName(Config().log_level)
    )
    args = parser.parse_args()

    level = getattr(logging, args.log_level.upper(), Config().log_level)
    configure(Config(board_size=args.board_size, log_level=level))

    logger.info("Configured board size: %s", args.board_size)
    board = Chessboard()
    logger.info("Created board with size %s", board.BOARD_SIZE)


if __name__ == "__main__":
    main()

