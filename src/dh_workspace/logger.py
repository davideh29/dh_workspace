import logging

logger = logging.getLogger("dh_workspace")
_handler = logging.StreamHandler()
_formatter = logging.Formatter("[%(levelname)s] %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False
