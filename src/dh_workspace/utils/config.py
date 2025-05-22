from dataclasses import dataclass
import logging


@dataclass
class Config:
    """Configuration for the package."""

    board_width: int = 8
    board_height: int = 8
    log_level: int = logging.INFO


CONFIG = Config()


def configure(config: Config) -> None:
    """Set global configuration and update logger level."""
    global CONFIG
    CONFIG = config
    from .logger import logger

    logger.setLevel(config.log_level)
