import argparse
import logging

from . import Chessboard, Config, configure, logger


def main() -> None:
    parser = argparse.ArgumentParser(description="dh_workspace entry point")
    parser.add_argument("--board-width", type=int, default=Config().board_width)
    parser.add_argument("--board-height", type=int, default=Config().board_height)
    parser.add_argument("--log-level", default=logging.getLevelName(Config().log_level))
    args = parser.parse_args()

    level = getattr(logging, args.log_level.upper(), Config().log_level)
    configure(
        Config(
            board_width=args.board_width,
            board_height=args.board_height,
            log_level=level,
        )
    )

    logger.info(
        "Configured board width %s height %s",
        args.board_width,
        args.board_height,
    )
    board = Chessboard()
    logger.info(
        "Created board with width %s and height %s",
        board.BOARD_WIDTH,
        board.BOARD_HEIGHT,
    )


if __name__ == "__main__":
    main()
